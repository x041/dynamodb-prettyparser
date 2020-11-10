from decimal import Decimal

def parseResults(records):
    recordsConv = []
    items = records.get('Items') or records.get('Item') or records

    if isinstance(items, dict):
        is_single = True
        items = [items]
    else:
        is_single = False

    def parseList(dynamoList):
        for d in dynamoList:
            dynamoType = list(d.keys())[0]
            dynamoConvItem = typeMap[dynamoType](d[dynamoType])
            dynamoConvList.append(dynamoConvItem)
        return dynamoConvList

    def parseMap(dynamoMap):
        for d in dynamoMap:
            dynamoType = list(dynamoMap[d].keys())[0]
            dynamoConvMap[d] = typeMap[dynamoType](dynamoMap[d][dynamoType])
        return dynamoConvMap

    typeMap = {
        'S': lambda x: x,
        'N': lambda x: (int, Decimal)[len(x.split('.')) - 1](x),
        'L': parseList,
        'B': lambda x: x,
        'BS': parseList,
        'BOOL': lambda x: x == 'true',
        'NS': parseList,
        'NULL': lambda x: None,
        'SS': list,
        'M': parseMap
    }

    for record in items:
        recordConv = {}
        for attributeName in record.keys():
            dynamoType = next(iter(record[attributeName]))
            val = typeMap[dynamoType](record[attributeName][dynamoType])
            recordConv[attributeName] = val
        recordsConv.append(recordConv)

    if is_single:
        recordsConv = recordsConv[0]
    return recordsConv
