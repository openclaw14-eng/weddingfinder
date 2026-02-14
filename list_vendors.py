import httpx

URL = 'https://gqlprwursgbgkfkwzkyb.supabase.co/rest/v1/vendors?select=*'
KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU'
headers = {'Authorization': f'Bearer {KEY}', 'apikey': KEY}

r = httpx.get(URL, headers=headers)
data = r.json()
print(f'Total count: {len(data)}')
for v in data:
    print(f"  - {v['name']} ({v['slug']})")
