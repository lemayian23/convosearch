@echo off
echo ConvoSearch Status Check
echo =======================

docker-compose ps

echo.
echo Testing API health...
curl -s http://localhost:8000/health || echo "API: Not running"

echo.
echo Recent tickets:
curl -s http://localhost:8000/api/tickets 2>nul | python -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'tickets' in data:
        print(f'Found {len(data[\"tickets\"])} tickets')
        for ticket in data['tickets'][:3]:
            print(f'  - {ticket[\"ticket_id\"]}: {ticket[\"classification\"]}')
    else:
        print('No tickets or API not reachable')
except:
    print('Could not fetch tickets')
"

pause