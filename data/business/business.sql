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

CREATE TABLE business_raw (
    Location_ID             text,
    Business_Account_Number int,
    Ownership_Name          text,
    DBA_Name                text,
    Street_Address          text,
    City                    text,
    State                   text,
    Zip_Code                float,
    Business_Start_Date     text,
    Business_End_Date       text,
    Location_Start_Date     text,
    Location_End_Date       text,
    Mail_Address            text,
    Mail_City_State_Zip     text,
    Class_Code              text,
    PBC_Code                text,
    Business_Location       text

);

CREATE TABLE business (
    ownership_name          text,
    dba_name                text,
    street_address          text,
    city                    text,
    state                   text,
    zip_code                float,
    class_code              text,
    pbc_code                int,
    lat                     float,
    lon                     float,
    major_class             text,
    minor_class             text,
    category                text
);


ALTER TABLE business_raw OWNER TO postgres;
ALTER TABLE business OWNER TO postgres;

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

