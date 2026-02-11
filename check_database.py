from supabase import create_client, Client
import json

# --- Configuration ---
SUPABASE_URL = "https://ifbknohkqfqplwvocksc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlmYmtub2hrcWZxcGx3dm9ja3NjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg4NjIyMjIsImV4cCI6MjA3NDQzODIyMn0.a5motl3g-arn6B-_JmL4J6WhmwacAkesfW1LnD52FQY"


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("="*70)
print("🔍 DATABASE DIAGNOSTIC TOOL")
print("="*70)

# 1. Total Records
print("\n1️⃣ TOTAL RECORDS:")
try:
    result = supabase.table('knowledge').select('id', count='exact').execute()
    print(f"   Total rows: {result.count}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 2. Records by Subject
print("\n2️⃣ RECORDS BY SUBJECT:")
try:
    result = supabase.table('knowledge').select('subject').execute()
    subjects = {}
    for row in result.data:
        subj = row.get('subject', 'NULL')
        if subj in subjects:
            subjects[subj] += 1
        else:
            subjects[subj] = 1
    
    # Sort by count
    sorted_subjects = sorted(subjects.items(), key=lambda x: x[1], reverse=True)
    for subj, count in sorted_subjects[:20]:  # Top 20
        print(f"   {subj}: {count} chunks")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 3. Search for "physics"
print("\n3️⃣ SEARCHING FOR 'PHYSICS':")
try:
    # Search in text_chunk
    result = supabase.table('knowledge') \
        .select('subject, text_chunk') \
        .ilike('text_chunk', '%physics%') \
        .limit(3) \
        .execute()
    
    print(f"   Found {len(result.data)} results in text_chunk")
    for i, row in enumerate(result.data, 1):
        print(f"\n   Result {i}:")
        print(f"   Subject: {row.get('subject', 'N/A')}")
        print(f"   Preview: {row['text_chunk'][:150]}...")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 4. Search in subject field
print("\n4️⃣ SEARCHING FOR 'PHYSICS' IN SUBJECT FIELD:")
try:
    result = supabase.table('knowledge') \
        .select('subject, text_chunk') \
        .ilike('subject', '%physics%') \
        .limit(3) \
        .execute()
    
    print(f"   Found {len(result.data)} results in subject field")
    for i, row in enumerate(result.data, 1):
        print(f"\n   Result {i}:")
        print(f"   Subject: {row.get('subject', 'N/A')}")
        print(f"   Preview: {row['text_chunk'][:150]}...")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 5. Search for "biology"
print("\n5️⃣ SEARCHING FOR 'BIOLOGY':")
try:
    result = supabase.table('knowledge') \
        .select('subject, text_chunk') \
        .ilike('text_chunk', '%biology%') \
        .limit(3) \
        .execute()
    
    print(f"   Found {len(result.data)} results")
    for i, row in enumerate(result.data, 1):
        print(f"\n   Result {i}:")
        print(f"   Subject: {row.get('subject', 'N/A')}")
        print(f"   Preview: {row['text_chunk'][:150]}...")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 6. Check specific Physics subjects
print("\n6️⃣ CHECKING PHYSICS BOOK ENTRIES:")
physics_patterns = [
    'Physics_Book%',
    'physics%',
    'PHYSICS%',
    '%Physics%Chapter%'
]

for pattern in physics_patterns:
    try:
        result = supabase.table('knowledge') \
            .select('subject', count='exact') \
            .like('subject', pattern) \
            .limit(1) \
            .execute()
        
        if result.count and result.count > 0:
            print(f"   ✅ Pattern '{pattern}': {result.count} records")
            # Get sample
            sample = supabase.table('knowledge') \
                .select('subject') \
                .like('subject', pattern) \
                .limit(1) \
                .execute()
            if sample.data:
                print(f"      Example: {sample.data[0]['subject']}")
    except Exception as e:
        print(f"   ❌ Pattern '{pattern}': Error - {e}")

# 7. Sample random records
print("\n7️⃣ RANDOM SAMPLE (First 5 records):")
try:
    result = supabase.table('knowledge') \
        .select('id, subject, text_chunk') \
        .limit(5) \
        .execute()
    
    for row in result.data:
        print(f"\n   ID: {row['id']}")
        print(f"   Subject: {row.get('subject', 'NULL')}")
        print(f"   Text Preview: {row['text_chunk'][:100]}...")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 8. Check for Newton's Law specifically
print("\n8️⃣ SEARCHING FOR 'NEWTON' OR 'LAW OF INERTIA':")
try:
    result = supabase.table('knowledge') \
        .select('subject, text_chunk') \
        .ilike('text_chunk', '%newton%') \
        .limit(2) \
        .execute()
    
    print(f"   'Newton' found in {len(result.data)} chunks")
    
    result2 = supabase.table('knowledge') \
        .select('subject, text_chunk') \
        .ilike('text_chunk', '%inertia%') \
        .limit(2) \
        .execute()
    
    print(f"   'Inertia' found in {len(result2.data)} chunks")
    
    if result.data:
        print(f"\n   Sample Newton chunk:")
        print(f"   Subject: {result.data[0].get('subject', 'N/A')}")
        print(f"   Text: {result.data[0]['text_chunk'][:200]}...")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*70)
print("✅ DIAGNOSTIC COMPLETE")
print("="*70)
print("\n💡 NEXT STEPS:")
print("1. Check if Physics books are actually in the database")
print("2. Verify the 'subject' field format matches Biology format")
print("3. If Physics chunks exist, check their text content quality")
print("4. Consider re-uploading Physics PDFs if data is missing/corrupted")