# Data Book

## Overview

Folder | File | Description | Contents | Scale
:--|:--|:--|:--|:--
[assessment](https://data.sfgov.org/City-Management-and-Ethics/Secured-Property-Assessment-Roll-FY13-Q4/e6sm-rank) | Secured\_Property\_Assessment\_Roll\_FY13\_Q4.csv | Assessed property values | Address, taxable value, lat/lon | 204,541 samples, 26.7 MB
[business](https://data.sfgov.org/Economy-and-Community/Registered-Business-Locations-San-Francisco/g8m3-pdis) | <ul><li>Registered\_Business\_Locations\_-\_San\_Francisco.csv</li><li>[Principal\_Business_Code\_\_PBC\_\_List.csv](https://data.sfgov.org/Economy-and-Community/Principal-Business-Code-PBC-List/5cvm-h7xc)</li></ul> | Registered businesses | Address, 'class code', lat/lon | 156,111 samples, 38.2 MB
[sfpd](https://data.sfgov.org/Public-Safety/SFPD-Incidents-from-1-January-2003/tmnf-yvry) | SFPD\_Incidents\_-\_from\_1\_January\_2003.csv | SFPD incident reports from Jan 2003 - Oct 2015 | Date, time, Category, District, lat/lon | 1,830,772 incidents, 375.5 MB
[uscensus](http://factfinder.census.gov/) | <ul><li>ACS\_13\_5YR\_B19001.zip</li> <li>DEC\_10\_SF1\_P12.zip</li> <li>DEC\_10\_SF1\_H13.zip</li> <li>DEC\_10\_SF1\_P1.zip</li></ul> | <ul><li>Income, block group</li><li>Age/gender by block</li><li>Household size by block</li><li>Population by block</li></ul> | <ul><li>Income count, 16 buckets</li><li>Age/gender, 23 bins per gender</li><li>Household count, 1-7+ bin</li><li>Population count</li></ul> | block group: 582 samples; block: 7387 samples
[tiger](http://www.census.gov/geo/maps-data/data/tiger.html) | tlgdb\_2015\_a\_06\_ca.gdb.zip | Address to lat/lon lookup database, CA | | 219 MB (zipped)
[gpw](http://sedac.ciesin.columbia.edu/data/set/gpw-v3-population-density) | usa\_gpwv3\_pcount\_ascii\_25.zip | Gridded population of the world | Count on grid in 2.5 arc-minute buckets (0.042 deg) | Earth, 165 MB

## Postgres Schema

```
hoodie=# \d
             List of relations
 Schema |      Name      | Type  |  Owner
--------+----------------+-------+----------
 public | assessment     | table | postgres
 public | assessment_raw | table | postgres
 public | business       | table | postgres
 public | business_raw   | table | postgres
 public | sfpd           | table | postgres
 public | sfpd_raw       | table | postgres
 public | usc_age_gender | table | postgres
 public | usc_household  | table | postgres
 public | usc_pop        | table | postgres
 public | walkscore      | table | postgres
 public | walkscore_raw  | table | postgres
(11 rows)
```
```
hoodie=# \d assessment
           Table "public.assessment"
     Column      |       Type       | Modifiers
-----------------+------------------+-----------
 situs_address   | text             |
 situs_zip       | text             |
 apn             | text             |
 re              | double precision |
 re_improvements | double precision |
 pp_value        | double precision |
 district        | text             |
 taxable_value   | double precision |
 lat             | double precision |
 lon             | double precision |
```
```
hoodie=# \d assessment_raw
   Table "public.assessment_raw"
     Column      | Type | Modifiers
-----------------+------+-----------
 situs_address   | text |
 situs_zip       | text |
 apn             | text |
 re              | text |
 re_improvements | text |
 fixtures_value  | text |
 pp_value        | text |
 district        | text |
 taxable_value   | text |
 geom            | text |
```
```
hoodie=# \d business
            Table "public.business"
     Column     |       Type       | Modifiers
----------------+------------------+-----------
 ownership_name | text             |
 dba_name       | text             |
 street_address | text             |
 city           | text             |
 state          | text             |
 zip_code       | double precision |
 major_class    | text             |
 minor_class    | integer          |
 lat            | double precision |
 lon            | double precision |
```
```
hoodie=# \d business_raw
              Table "public.business_raw"
         Column          |       Type       | Modifiers
-------------------------+------------------+-----------
 location_id             | text             |
 business_account_number | integer          |
 ownership_name          | text             |
 dba_name                | text             |
 street_address          | text             |
 city                    | text             |
 state                   | text             |
 zip_code                | double precision |
 business_start_date     | text             |
 business_end_date       | text             |
 location_start_date     | text             |
 location_end_date       | text             |
 mail_address            | text             |
 mail_city_state_zip     | text             |
 class_code              | text             |
 pbc_code                | text             |
 business_location       | text             |
```
```
hoodie=# \d sfpd
                 Table "public.sfpd"
   Column   |            Type             | Modifiers
------------+-----------------------------+-----------
 category   | text                        |
 descript   | text                        |
 pddistrict | text                        |
 address    | text                        |
 lon        | double precision            |
 lat        | double precision            |
 datetime   | timestamp without time zone |
```
```
hoodie=# \d sfpd_raw
          Table "public.sfpd_raw"
   Column   |       Type       | Modifiers
------------+------------------+-----------
 incidntnum | text             |
 category   | text             |
 descript   | text             |
 dayofweek  | text             |
 date       | text             |
 time       | text             |
 pddistrict | text             |
 resolution | text             |
 address    | text             |
 x          | double precision |
 y          | double precision |
 location   | text             |
 pdid       | double precision |
```
```
hoodie=# \d usc_age_gender
       Table "public.usc_age_gender"
   Column    |       Type       | Modifiers
-------------+------------------+-----------
 block       | double precision |
 block_group | integer          |
 tract       | integer          |
 total       | integer          |
 m           | integer          |
 m_u5        | integer          |
 m_5_9       | integer          |
 m_10_14     | integer          |
 m_15_17     | integer          |
 m_18_19     | integer          |
 m_20        | integer          |
 m_21        | integer          |
 m_22_24     | integer          |
 m_25_29     | integer          |
 m_30_34     | integer          |
 m_35_39     | integer          |
 m_40_44     | integer          |
 m_45_49     | integer          |
 m_50_54     | integer          |
 m_55_59     | integer          |
 m_60_61     | integer          |
 m_62_64     | integer          |
 m_65_66     | integer          |
 m_67_69     | integer          |
 m_70_74     | integer          |
 m_75_79     | integer          |
 m_80_84     | integer          |
 m_85_over   | integer          |
 f           | integer          |
 f_u5        | integer          |
 f_5_9       | integer          |
 f_10_14     | integer          |
 f_15_17     | integer          |
 f_18_19     | integer          |
 f_20        | integer          |
 f_21        | integer          |
 f_22_24     | integer          |
 f_25_29     | integer          |
 f_30_34     | integer          |
 f_35_39     | integer          |
 f_40_44     | integer          |
 f_45_49     | integer          |
 f_50_54     | integer          |
 f_55_59     | integer          |
 f_60_61     | integer          |
 f_62_64     | integer          |
 f_65_66     | integer          |
 f_67_69     | integer          |
 f_70_74     | integer          |
 f_75_79     | integer          |
 f_80_84     | integer          |
 f_85_over   | integer          |
```
```
hoodie=# \d usc_household
        Table "public.usc_household"
   Column    |       Type       | Modifiers
-------------+------------------+-----------
 block       | double precision |
 block_group | integer          |
 tract       | integer          |
 total       | integer          |
 p1          | integer          |
 p2          | integer          |
 p3          | integer          |
 p4          | integer          |
 p5          | integer          |
 p6          | integer          |
 p7          | integer          |
```
```
hoodie=# \d usc_pop
           Table "public.usc_pop"
   Column    |       Type       | Modifiers
-------------+------------------+-----------
 block       | double precision |
 block_group | integer          |
 tract       | integer          |
 total       | integer          |
```
```
hoodie=# \d walkscore
                Table "public.walkscore"
    Column    |            Type             | Modifiers
--------------+-----------------------------+-----------
 snapped_lat  | double precision            |
 snapped_lon  | double precision            |
 walkscore    | integer                     |
 description  | text                        |
 updated      | timestamp without time zone |
 searched_lat | double precision            |
 searched_lon | double precision            |
```
```
hoodie=# \d walkscore_raw
               Table "public.walkscore_raw"
     Column     |            Type             | Modifiers
----------------+-----------------------------+-----------
 description    | text                        |
 help_link      | text                        |
 logo_url       | text                        |
 more_info_icon | text                        |
 more_info_link | text                        |
 snapped_lat    | double precision            |
 snapped_lon    | double precision            |
 status         | integer                     |
 updated        | timestamp without time zone |
 walkscore      | text                        |
 ws_link        | text                        |
 searched_lat   | double precision            |
 searched_lon   | double precision            |
```