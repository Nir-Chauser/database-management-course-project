from django.shortcuts import render
from django.db.models import Avg
from django.db import connection
from .models import Owners, Apartments, Rentals
from datetime import datetime

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def home(request):
    return render(request, 'home.html')

def query_results(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT mcp.aID, mcp.renterID
            FROM MaxCostPerApartment mcp
            JOIN Apartments a ON mcp.aID = a.aID
            JOIN LegalOwners lo ON a.ownerID = lo.ownerID
            JOIN ApartmentsRentedMax3Years arm3 ON mcp.aID = arm3.aID
            ORDER BY mcp.aID ASC, mcp.renterID ASC
        """)
        query1_results = dictfetchall(cursor)

        cursor.execute("""
            SELECT DISTINCT a.city
            FROM MinimalistRentals mr
            JOIN Apartments a ON mr.aID = a.aID
            ORDER BY a.city ASC
        """)
        query2_results = dictfetchall(cursor)

        cursor.execute("""
            SELECT o.oName, o.bDate,
                   COUNT(DISTINCT r.aID) as problematic_apartments
            FROM Owners o
            JOIN DiverseOwners do ON o.ownerID = do.ownerID
            JOIN Apartments a ON o.ownerID = a.ownerID
            JOIN Rentals r ON a.aID = r.aID
            JOIN ProblematicRenters pr ON r.renterID = pr.renterID
            WHERE YEAR(o.bDate) >= 2000
            GROUP BY o.ownerID, o.oName, o.bDate
            ORDER BY o.bDate DESC, o.ownerID ASC
        """)
        query3_results = dictfetchall(cursor)

    return render(request, 'query_results.html', {
        'query1_results': query1_results,
        'query2_results': query2_results,
        'query3_results': query3_results,
    })

def add_rental(request):
    from django.utils.timezone import now
    message = ''
    error = ''
    warning = ''
    current_year = now().year
    apartments = Apartments.objects.all()

    if request.method == 'POST':
        try:
            renterid = int(request.POST.get('renter_id'))
            cost = int(request.POST.get('cost'))
            aid = int(request.POST.get('aid'))

            if renterid <= 0:
                error = "Renter ID must be a positive integer."
            elif cost <= 500:
                error = "Monthly cost must be greater than 500."
            else:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT 1 FROM Rentals
                        WHERE renterID = %s AND rYear = %s
                    """, [renterid, current_year])
                    if cursor.fetchone():
                        error = "Rental for this renter and year already exists."
                    else:
                        cursor.execute("""
                            SELECT 1 FROM Rentals
                            WHERE renterID = %s
                        """, [renterid])
                        if not cursor.fetchone():
                            error = "Renter ID does not exist in the system."
            if not error:
                Rentals.objects.create(renterid=renterid, ryear=current_year, aid_id=aid, cost=cost)
                message = "Rental added successfully."
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT COUNT(DISTINCT renterID) AS cnt
                        FROM Rentals
                        WHERE aID = %s AND rYear = %s
                    """, [aid, current_year])
                    result = dictfetchall(cursor)
                    if result and result[0]['cnt'] > 5:
                        warning = "Warning: More than 5 renters for this apartment in the same year."

        except Exception as e:
            error = f"Unexpected error: {str(e)}"

    return render(request, 'add_rental.html', {
        'apartments': apartments,
        'message': message + (' ' + warning if warning else ''),
        'error': error
    })

def search_analysis(request):
    name_prefix = request.GET.get('name_prefix', '').strip()
    owner_id = request.GET.get('owner_id', '').strip()
    search_type = request.GET.get('search_type', '')

    owners = []
    owner_stats = None
    error = ''

    if search_type == 'find' and name_prefix:
        owners = list(Owners.objects.filter(oname__istartswith=name_prefix).values(
            'ownerid', 'oname'
        ))
        if not owners:
            error = "No owners found with that prefix."

    elif search_type == 'analyze' and owner_id:
        try:
            owner_id = int(owner_id)
            owner = Owners.objects.get(ownerid=owner_id)
            num_apartments = Apartments.objects.filter(ownerid=owner_id).count()

            if num_apartments == 0:
                avg_roommates = 'NA'
            else:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT AVG(CAST(sub.num_roommates AS FLOAT)) AS avg_roommates
                        FROM (
                            SELECT COUNT(DISTINCT renterID) AS num_roommates
                            FROM Rentals r
                            JOIN Apartments a ON r.aID = a.aID
                            WHERE a.ownerID = %s
                            GROUP BY r.aID, r.rYear
                            HAVING COUNT(*) > 0
                        ) AS sub;
                    """, [owner_id])
                    result = dictfetchall(cursor)
                    avg_val = result[0]['avg_roommates']
                    avg_roommates = avg_val if avg_val is not None else 'NA'

            others_in_city = Owners.objects.filter(
                residencecity=owner.residencecity
            ).exclude(ownerid=owner_id).count()

            owner_stats = {
                'num_apartments': num_apartments,
                'avg_roommates': avg_roommates,
                'num_owners_in_city': others_in_city
            }

        except Owners.DoesNotExist:
            error = 'Owner not found.'
        except ValueError:
            error = 'Invalid owner ID.'
        except Exception as e:
            error = f'Unexpected error: {str(e)}'

    return render(request, 'search_analysis.html', {
        'owners': owners,
        'owner_stats': owner_stats,
        'name_prefix': name_prefix,
        'owner_id': owner_id,
        'error': error
    })