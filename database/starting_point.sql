--
-- PostgreSQL database dump
--

-- Dumped from database version 13.3 (Debian 13.3-1.pgdg100+1)
-- Dumped by pg_dump version 13.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.id_seq OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: repository; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."repository" (
    id bigint DEFAULT nextval('public.id_seq'::regclass) NOT NULL,
    name character varying(255),
    language character varying(50),
    commits integer,
    tests boolean DEFAULT false,
    ci_cd boolean DEFAULT false,
    create_date timestamp(6) without time zone DEFAULT now()
);


ALTER TABLE public."repository" OWNER TO postgres;

--
-- Data for Name: repository; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."repository" (id, name, language, commits, tests, ci_cd, create_date) FROM stdin;
\.


--
-- Name: id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.id_seq', 1, false);


--
-- Name: repository repository_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."repository"
    ADD CONSTRAINT "repository_pkey" PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

