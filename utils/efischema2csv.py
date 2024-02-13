# Following RFC 8259 each Json Value must be one of object, array, number, or string, or one of
# the following three literal names: false, null, true

# Everything has to be in UTF-8

# JSON Validation Vocabulary https://datatracker.ietf.org/doc/html/draft-bhutton-json-schema-validation-01

# ! CHECKOUT: https://json-schema.org/understanding-json-schema/reference/array.html

import argparse
import json
import csv
import sys

def loop_prop(input,lev,pos_number):
    count=1
    list = get_required_list(input)
    for val in get_prop_list(input):
        pos_number = get_pos_number(lev,pos_number,count)
        req = check_if_required(val,list)
        if type(input['properties'][val]) == dict:
            if 'type' in input['properties'][val].keys():
                ttype = input['properties'][val]['type']
                if ttype == 'array':
                    # Does the array contain further objects or is at an array of basic types?
                    if type(input['properties'][val]['items']) == dict:
                        if 'properties' in input['properties'][val]['items']:
                            write_row(pos_number,val,req+'-n','array','array of subelements',input['properties'][val]['description'])
                            #print('OUT: ',pos_number,val,req+'-n','array')
                            loop_prop(input['properties'][val]['items'],lev+1,pos_number)
                        else:
                            val_type = input['properties'][val]['items']['type']
                            val_constrain = get_constrains(input['properties'][val]['items'])
                            write_row(pos_number,val,req+'-n',val_type,val_constrain,input['properties'][val]['description'])
                            #print('OUT: ',pos_number,val,req+'-n',val_type,val_constrain)
                    else:
                        if (len(input['properties'][val]['items']) > 1):
                            val_type = 'array of ['
                            val_constrain = []
                            looplen = len(input['properties'][val]['items'])
                            for i in range(looplen):
                                val_type += input['properties'][val]['items'][i]['type']
                                if i < looplen-1: val_type += ', '
                                val_constrain.append(get_constrains(input['properties'][val]['items'][i]))
                            val_type += ']'
                            write_row(pos_number,val,req+'-n',val_type,val_constrain,input['properties'][val]['description'])
                            #print('OUT: ',pos_number,val,req+'-n',val_type,val_constrain)
                        else:
                            print('ERROR: ',val,'is array of length 1')
                elif ttype == 'object':
                    if req == '0': req='0-1'
                    write_row(pos_number,val,req,'object','object of subelement',input['properties'][val]['description'])
                    #print('OUT: ',pos_number,val,req,'object')
                    loop_prop(input['properties'][val],lev+1,pos_number)
                elif ttype == 'number':
                    print('ERROR: ',val,'number')
                elif ttype == 'interger':
                    if req == '0': req='0-1'
                    write_row(pos_number,val,req,'integer',get_constrains(input['properties'][val]),input['properties'][val]['description'])
                    #print('OUT: ',pos_number,val,req,'integer',get_constrains(input['properties'][val]))
                elif ttype == 'string':
                    if req == '0': req='0-1'
                    write_row(pos_number,val,req,'string',get_constrains(input['properties'][val]),input['properties'][val]['description'])
                    #print('OUT: ',pos_number,val,req,'string',get_constrains(input['properties'][val]))
                elif type(ttype) == bool:
                    print('ERROR: ',val,'boolean')
                else:
                    print('ERROR: ',val,' does not contain a known type')
            else:
                print('ERROR: ',val,' does not contain "type" as key')
        else:
            print('DEBUG: ',val,' is not a dict')

        count +=1


def get_constrains(input_dict):
    constrains=[]
    if 'pattern' in input_dict:
        constrains.append(input_dict['pattern'])
    if 'enum' in input_dict:
        constrains.append('controlled list')
    if 'maxLength' in input_dict:
        constrains.append('maxLength'+str(input_dict['maxLength']))
    return constrains

def get_allowed_values(val,input):
    if 'enum' in input['properties'][val]:
        if 'type' in input['properties'][val]:
            return 'controlled list of type: '+ input['properties'][val]['type']
        else:
            return 'controlled list'
    elif 'items' in input['properties'][val]:
        if 'enum' in input['properties'][val]['items']:
            return 'controlled list of type: '+ input['properties'][val]['items']['type']
        else:
            return 'array of subelements'
    else:
        #return 'object'
        if not input['properties'][val]['type'] in ['object']:
            return input['properties'][val]['type']
        else:
            return ''

def get_pos_number(lev,pos_number,count):
    pos = str(count).zfill(2)
    if lev == 1: position = 0
    if lev == 2: position = 2
    if lev == 3: position = 4
    if lev == 4: position = 6
    temp = list(pos_number)
    temp[position:position+2] = pos
    pos_number = "".join(temp)
    return pos_number

def get_required_list(input):
    if 'required' in input.keys():
        return input['required']
    else:
        return []

def get_prop_list(input):
    if type(input) == dict:
        if 'properties' in input.keys():
            return input['properties']
        else:
            return []
    else:
        return []

def check_if_required(val,reqlist):
    if val in reqlist:
        return '1'
    else:
        return '0'
    
def write_row(pos_number,val,cardinality,dtype,constrains,description):
    number = pos_number[0:2].lstrip('0')
    if len(pos_number) > 3: number = number + '.' + pos_number[2:4].lstrip('0')
    if len(pos_number) > 5: number = number + '.' + pos_number[4:6].lstrip('0')
    if len(pos_number) > 7: number = number + '.' + pos_number[6:8].lstrip('0')
    
    row = [number,val,cardinality,dtype,constrains,description]
    writer.writerow(row)
        

######## MAIN ########################
def main(args=None, json_input=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', metavar='FILE',
        type=argparse.FileType('r'), default=sys.stdin,
        help='Read input from FILE instead of stdin.')
    parser.add_argument(
        '-o', '--output', metavar='FILE',
        type=argparse.FileType('w'), default=sys.stdout,
        help='Write output to FILE instead of stdout.')
    args = parser.parse_args()

    ##### Parameters ########

    if json_input:
        jsondata = json_input
    else:
        jsondata = json.loads(args.input.read())

    top_level_properties = jsondata['properties']
    if len(top_level_properties) != 1:
        raise ValueError(
            f"Expect exactly one key in top-level properties of input data,"
            f" found: {top_level_properties.keys()}")
    level1 = list(top_level_properties.values())[0]

    global writer
    writer = csv.writer(args.output)

    row = ['Id','Name','Cardinality','Type','Constraints','Definition']

    writer.writerow(row)

    loop_prop(level1,1,'00')

if __name__ == '__main__':
    main()
