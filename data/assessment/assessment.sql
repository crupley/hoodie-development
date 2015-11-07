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

CREATE TABLE assessment_raw (
    Situs_Address       text,
    Situs_Zip           text,
    APN                 text,
    RE                  text,
    RE_Improvements     text,
    Fixtures_Value      text,
    PP_Value            text,
    District            text,
    Taxable_Value       text,
    geom                text
);

CREATE TABLE assessment (
    Situs_Address       text,
    Situs_Zip           text,
    APN                 text,
    RE                  float,
    RE_Improvements     float,
    PP_Value            float,
    District            text,
    Taxable_Value       float,
    lat                 float,
    lon                 float
);


ALTER TABLE assessment_raw OWNER TO postgres;
ALTER TABLE assessment OWNER TO postgres;
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

