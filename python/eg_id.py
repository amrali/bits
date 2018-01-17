# Egypt national ID consists of 14 digits.
# [2] [3 4 5 2 6 9] [4 5] [7 7 5 2] [5]
#
# The first segment defines the decade in which the person was born.
# (e.g., if 2 then the person was born between 1900 and 1999 and if 3 then
# the person was born between 2000 and 2099)
#
# The second segment is the birth date of the person. (e.g., 8 3 0 7 0 5 means
# the person was born on the 5th of July 1983)
#
# The third segment is the directorate the person was born into according to
# the following table:
# Cairo 01
# Alexandria 02
# Port Said 03
# Suez 04
# Damietta 11
# El Dakahlia 12
# Al Sharqia 13
# Qalyubia 14
# Kafr El Sheikh 15
# Al Gharbia 16
# Monufia 17
# Beheira 18
# Ismailia 19
# Giza 21
# Beni Suef 22
# Faiyum 23
# Minya 24
# Asyut 25
# Sohag 26
# Qena 27
# Aswan 28
# Luxor 29
# Red Sea 31
# New Valley 32
# Matrouh 33
# North Sinai 34
# South Sinai 35
# Outside Egypt 88
#
# The fourth segment is the person's sequence of birth on gov computers on the
# day of birth. The last digit of that sequence defines the person's sex.
# If the last digit is odd then the person is male and if even the person is female.
# (e.g., 1, 3, 5, 7, 9 is male, while 2, 4, 6, 8 is female)
#
# The fifth and last segment is a check sum digit in the range [1, 9].
#
# The number under the Eagle is the ID of the factory that issued the ID card.

segment_1 = {
        '0': '1700 - 1799',
        '1': '1800 - 1899',
        '2': '1900 - 1999',
        '3': '2000 - 2099'}

segment_3 = {
        '01': 'Cairo',
        '02': 'Alexandria',
        '03': 'Port Said',
        '04': 'Suez',
        '11': 'Damietta',
        '12': 'El Dakahlia',
        '13': 'Al Sharqia',
        '14': 'Qalyubia',
        '15': 'Kafr El Sheikh',
        '16': 'Al Gharbia',
        '17': 'Monufia',
        '18': 'Beheira',
        '19': 'Ismailia',
        '21': 'Giza',
        '22': 'Beni Suef',
        '23': 'Faiyum',
        '24': 'Minya',
        '25': 'Asyut',
        '26': 'Sohag',
        '27': 'Qena',
        '28': 'Aswan',
        '29': 'Luxor',
        '31': 'Red Sea',
        '32': 'New Valley',
        '33': 'Matrouh',
        '34': 'North Sinai',
        '35': 'South Sinai',
        '88': 'Outside Egypt'}

segment_4 = lambda x: 'male' if int(x) % 2 else 'female'

digits_of = lambda n: [int(i) for i in str(n)]

def checksum(eid):
    digits = digits_of(eid[:-1]) # remove checksum digit
    s_odd = sum(digits[::2])
    s_even = sum(digits[1::2])
    csum = (s_even + s_odd * 3) % 10
    return csum

if __name__ == '__main__':
    print("Example ID: 12345678901234")
    eid = input("Please enter your national ID: ")

    print()
    seg_1 = eid[0:1]
    seg_2 = eid[1:7]
    seg_3 = eid[7:9]
    seg_4 = eid[9:13]
    seg_5 = eid[13:14]

    print("The person was born in the decade: {}".format(segment_1[seg_1]))
    print("The person birth date is: {}".format(seg_2))
    print("The person was born in: {}".format(segment_3[seg_3]))
    print("The person is: {}".format(segment_4(seg_4)))
    print("The checksum is: {} {}".format(checksum(eid), seg_5))
