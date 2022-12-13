



# admin group - 'admin', 본인pc만 - 'uniGroup', 본인 + 수집pc제어 - 'multiGroup'
user_info = {
    'LEEHANEUL': {
        'id' : 'LEEHANEUL',
        'name' : '이한을',
        'group' : 'uniGroup', 
        'mac_adr' : 'B8-97-5A-A9-62-3B'
        },

    'rullru': {
        'id' : 'rullru',
        'name' : '신준영',
        'group' : 'uniGroup', 
        'mac_adr' : ''
        },

    'slkma': {
        'id' : 'slkma',
        'name' : '이민아',
        'group' : 'multiGroup', 
        'mac_adr' : 'A8-A1-59-A7-79-A8'
        },

    'wjswjs001204': {
        'id' : 'wjswjs001204',
        'name' : '원재승',
        'group' : 'mutliGroup', 
        'mac_adr' : 'A8-A1-59-A7-7A-69'
        },

    'jhjung' : {
        'id' : 'jhjung',
        'name' : '정재희',
        'group' : 'multiGroup',
        'mac_adr' : 'D8-BB-C1-5B-6A-FC'
        },
        
    'sdfjkl123': {
        'id' : 'sdfjkl123',
        'name' : '변진환',
        'group' : 'multiGroup', 
        'mac_adr' : '70-85-C2-54-53-B4'
        },

    'sylee': {
        'id' : 'sylee',
        'name' : '이서연',
        'group' : 'admin', 
        'mac_adr' : 'D8-BB-C1-5B-60-31'
        }
}


name_list = [ Info['name'] for Info in user_info.values() ]
adrs_dict = { Info['name'] : Info['mac_adr'] for Info in user_info.values() } # name : mac_adr


if __name__ == '__main__':
    # print(adrs_dict)
    print(user_info)


