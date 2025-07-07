# idea for flow

1) incoming home listing
    - is < 200k
    - geocode to obtain lat/lon
    - is in bounding box of upper NE usa?
    - has desirable diversity index value
2) find closest airport (less amount of airports, this is less expensive)
3) google maps api 
    - is <2 hours
4) find closest weather data (expensive distance calc)
    - is TRUTH (whatever condition we decide on)
5) if you make it this far -> save

# Runtimes

However we can fetch listing data from might change this. Maybe we only fetch from certain states we know ahead of time.

- end state - bot scrapes daily and emails list of homes
- time machine - setup configuration that sets parameters/filters and runs for listing date or most recent X?