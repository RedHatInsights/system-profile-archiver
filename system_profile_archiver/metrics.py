from prometheus_client import Counter, Histogram


inventory_service_requests = Histogram(
    "spa_inventory_service_requests", "inventory service call stats"
)

inventory_service_exceptions = Counter(
    "spa_inventory_service_exceptions", "count of exceptions raised by inv service"
)

# kerlescan expects this to be Histogram
inventory_service_no_profile = Histogram(
    "spa_inventory_service_no_profile", "count of systems fetched without a profile",
)
