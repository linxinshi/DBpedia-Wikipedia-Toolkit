# usage
command: python extract_mapping_based_properties_object.py FILENAME
# input
DBpedia mapping_based_properties_object dataset in ttl format
# output
uri, property, value (seperated by tab)
# parameters
set DEBUG_MODE=True if you want to output results to the console  
set MONGO_MODE=True if you want to store results into the mongoDB
# behaviour
the program will print 'error' when it cannot analyze a line
# other
works fine with DBpedia 2015-10
# notice
the type of value is always uri in mapping_based_properties_object dataset
