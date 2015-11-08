--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: events; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE usc_age_gender (
    Block       float,
    Block_Group int,
    Tract       int,
    Id2         text,
    Total       int,
    M           int,
    M_U5        int,
    M_5_9       int,
    M_10_14     int,
    M_15_17     int,
    M_18_19     int,
    M_20        int,
    M_21        int,
    M_22_24     int,
    M_25_29     int,
    M_30_34     int,
    M_35_39     int,
    M_40_44     int,
    M_45_49     int,
    M_50_54     int,
    M_55_59     int,
    M_60_61     int,
    M_62_64     int,
    M_65_66     int,
    M_67_69     int,
    M_70_74     int,
    M_75_79     int,
    M_80_84     int,
    M_85_over   int,
    F           int,
    F_U5        int,
    F_5_9       int,
    F_10_14     int,
    F_15_17     int,
    F_18_19     int,
    F_20        int,
    F_21        int,
    F_22_24     int,
    F_25_29     int,
    F_30_34     int,
    F_35_39     int,
    F_40_44     int,
    F_45_49     int,
    F_50_54     int,
    F_55_59     int,
    F_60_61     int,
    F_62_64     int,
    F_65_66     int,
    F_67_69     int,
    F_70_74     int,
    F_75_79     int,
    F_80_84     int,
    F_85_over   int
);

CREATE TABLE usc_household (
    Block       float,
    Block_Group int,
    Tract       int,
    Id2         text,
    Total       int,
    p1          int,
    p2          int,
    p3          int,
    p4          int,
    p5          int,
    p6          int,
    p7          int
);

CREATE TABLE usc_pop (
    Block       float,
    Block_Group int,
    Tract       int,
    Id2         text,
    Total       int
);

CREATE TABLE usc_shapefile (
    state       text,
    county      text,
    tract       text,
    block       text,
    geoid       text,
    name        text,
    mtfcc       text,
    land_area   int,
    water_area  int,
    lat         float,
    lon         float
);

ALTER TABLE usc_age_gender OWNER TO postgres;
ALTER TABLE usc_household OWNER TO postgres;
ALTER TABLE usc_pop OWNER TO postgres;
ALTER TABLE usc_shapefile OWNER TO postgres;



--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

