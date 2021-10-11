from storm_client import Storm

service = Storm("http://127.0.0.1:5000", "my-token")

#
# 1. List projects
#
print(service.project.search())

#
# 2. Get specific project
#
print(service.project.resolve(1))
