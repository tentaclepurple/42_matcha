import requests

def generate_profiles(n):
    profiles = []
    for _ in range(n):
        response = requests.get("https://randomuser.me/api/?nat=es")
        if response.status_code == 200:
            user = response.json()['results'][0]
            print(user)
            print()
            profile = {
                'name': f"{user['name']['first']} {user['name']['last']}",
                'age': user['dob']['age'],
                'email': user['email'],
                'location': f"{user['location']['city']}, {user['location']['country']}",
                'picture': user['picture']['large'],
            }
            profiles.append(profile)
    return profiles

# Genera 5 perfiles
profiles = generate_profiles(5)
for profile in profiles:
    print()
    print(profile)
