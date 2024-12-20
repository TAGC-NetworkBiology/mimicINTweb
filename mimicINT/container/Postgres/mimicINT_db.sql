--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.19
-- Dumped by pg_dump version 9.6.19

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
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO django;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: django
--

CREATE TABLE public.auth_group (
    id integer DEFAULT nextval('public.auth_group_id_seq'::regclass) NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO django;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO django;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO django;

--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO django;

--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: django
--

CREATE TABLE public.auth_user (
    id integer DEFAULT nextval('public.auth_user_id_seq'::regclass) NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO django;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO django;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: django
--

CREATE TABLE public.auth_user_groups (
    id integer DEFAULT nextval('public.auth_user_groups_id_seq'::regclass) NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO django;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO django;

--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: django
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO django;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO django;

--
-- Name: django_admin_log_id_seq1; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE public.django_admin_log_id_seq1
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq1 OWNER TO django;

--
-- Name: django_admin_log_id_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: django
--

ALTER SEQUENCE public.django_admin_log_id_seq1 OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO django;

--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: django
--

CREATE TABLE public.django_content_type (
    id integer DEFAULT nextval('public.django_content_type_id_seq'::regclass) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO django;

--
-- Name: django_flatpage_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE public.django_flatpage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_flatpage_id_seq OWNER TO django;

--
-- Name: django_flatpage; Type: TABLE; Schema: public; Owner: django
--

CREATE TABLE public.django_flatpage (
    id integer DEFAULT nextval('public.django_flatpage_id_seq'::regclass) NOT NULL,
    url character varying(100) NOT NULL,
    title character varying(200) NOT NULL,
    content text NOT NULL,
    enable_comments boolean NOT NULL,
    template_name character varying(70) NOT NULL,
    registration_required boolean NOT NULL
);


ALTER TABLE public.django_flatpage OWNER TO django;

--
-- Name: django_flatpage_sites_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE public.django_flatpage_sites_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_flatpage_sites_id_seq OWNER TO django;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO django;

--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: django
--

CREATE TABLE public.django_migrations (
    id integer DEFAULT nextval('public.django_migrations_id_seq'::regclass) NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO django;

--
-- Name: django_session; Type: TABLE; Schema: public; Owner: django
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO django;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: django
--

CREATE SEQUENCE public.django_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_site_id_seq OWNER TO django;

--
-- Name: django_site; Type: TABLE; Schema: public; Owner: django
--

CREATE TABLE public.django_site (
    id integer DEFAULT nextval('public.django_site_id_seq'::regclass) NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.django_site OWNER TO django;

--
-- Name: mimicINTapp_home_text; Type: TABLE; Schema: public; Owner: django
--

CREATE TABLE public."mimicINTapp_home_text" (
    "text_ID" integer NOT NULL,
    text_title text,
    text_content text
);


ALTER TABLE public."mimicINTapp_home_text" OWNER TO django;

--
-- Name: mimicINTapp_job_infos; Type: TABLE; Schema: public; Owner: django
--

CREATE TABLE public."mimicINTapp_job_infos" (
    job_id character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    submission_date timestamp without time zone NOT NULL,
    status character varying(255) NOT NULL,
    run_name character varying(255) NOT NULL,
    target_name character varying(255) NOT NULL,
    query_name character varying(255) NOT NULL,
    about text NOT NULL
);


ALTER TABLE public."mimicINTapp_job_infos" OWNER TO django;

--
-- Name: mimicINTapp_news_part; Type: TABLE; Schema: public; Owner: django
--

CREATE TABLE public."mimicINTapp_news_part" (
    "news_ID" integer NOT NULL,
    news_title text,
    news_content text
);


ALTER TABLE public."mimicINTapp_news_part" OWNER TO django;

--
-- Name: mimicINTapp_output_file; Type: TABLE; Schema: public; Owner: django
--

CREATE TABLE public."mimicINTapp_output_file" (
    file_accession text NOT NULL,
    file_description text,
    file_path text,
    rule_id text
);


ALTER TABLE public."mimicINTapp_output_file" OWNER TO django;

--
-- Name: mimicINTapp_pipeline_rule; Type: TABLE; Schema: public; Owner: django
--

CREATE TABLE public."mimicINTapp_pipeline_rule" (
    rule_id text NOT NULL,
    rule_order integer,
    rule_description text,
    rule_duration integer,
    log_path text
);


ALTER TABLE public."mimicINTapp_pipeline_rule" OWNER TO django;

--
-- Name: mimicINTapp_setting_prediction; Type: TABLE; Schema: public; Owner: django
--

CREATE TABLE public."mimicINTapp_setting_prediction" (
    "setting_ID" integer NOT NULL,
    setting_name text,
    tooltip text
);


ALTER TABLE public."mimicINTapp_setting_prediction" OWNER TO django;

--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: django
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq1'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 1, false);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$150000$lEMcu80AiGog$BcXntbVIADChpDat8EXymp8fmMOCwde3UM8Hoa84n0Y=	2024-03-15 13:00:29.81578+00	t	mimicint			andreas.zanzoni@inserm.fr	t	t	2024-03-01 11:38:08.430257+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 1, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2024-03-15 13:03:26.068402+00	1	news_part object (1)	2	[]	7	1
2	2024-03-15 13:08:32.930055+00	0	news_part object (0)	1	[{"added": {}}]	7	1
3	2024-03-15 13:09:09.294755+00	0	news_part object (0)	1	[{"added": {}}]	7	1
4	2024-03-15 13:09:41.908146+00	0	news_part object (0)	1	[{"added": {}}]	7	1
5	2024-03-15 13:10:03.409548+00	0	news_part object (0)	1	[{"added": {}}]	7	1
\.


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq1; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq1', 5, true);


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	mimicINTapp	news_part
8	mimicINTapp	setting_prediction
9	mimicINTapp	home_text
10	mimicINTapp	output_file
11	mimicINTapp	pipeline_rule
12	mimicINTapp	job_infos
13	sites	site
14	flatpages	flatpage
\.


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 1, false);


--
-- Data for Name: django_flatpage; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public.django_flatpage (id, url, title, content, enable_comments, template_name, registration_required) FROM stdin;
\.


--
-- Name: django_flatpage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.django_flatpage_id_seq', 1, false);


--
-- Name: django_flatpage_sites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.django_flatpage_sites_id_seq', 1, false);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2021-04-23 13:01:26.76042+00
2	auth	0001_initial	2021-04-23 13:01:27.079429+00
3	admin	0001_initial	2021-04-23 13:01:27.641303+00
4	admin	0002_logentry_remove_auto_add	2021-04-23 13:01:27.741385+00
5	admin	0003_logentry_add_action_flag_choices	2021-04-23 13:01:27.775988+00
6	contenttypes	0002_remove_content_type_name	2021-04-23 13:01:27.807112+00
7	auth	0002_alter_permission_name_max_length	2021-04-23 13:01:27.821118+00
8	auth	0003_alter_user_email_max_length	2021-04-23 13:01:27.838709+00
9	auth	0004_alter_user_username_opts	2021-04-23 13:01:27.861172+00
10	auth	0005_alter_user_last_login_null	2021-04-23 13:01:27.878539+00
11	auth	0006_require_contenttypes_0002	2021-04-23 13:01:27.888493+00
12	auth	0007_alter_validators_add_error_messages	2021-04-23 13:01:27.916567+00
13	auth	0008_alter_user_username_max_length	2021-04-23 13:01:27.966417+00
14	auth	0009_alter_user_last_name_max_length	2021-04-23 13:01:28.016681+00
15	auth	0010_alter_group_name_max_length	2021-04-23 13:01:28.046405+00
16	auth	0011_update_proxy_permissions	2021-04-23 13:01:28.064706+00
17	sites	0001_initial	2021-04-23 13:01:28.108217+00
18	flatpages	0001_initial	2021-04-23 13:01:28.259518+00
19	mimicINTapp	0001_initial	2021-04-23 13:01:28.562122+00
20	mimicINTapp	0002_home_text	2021-04-23 13:01:28.672345+00
21	mimicINTapp	0003_output_file	2021-04-23 13:01:28.754679+00
22	mimicINTapp	0004_pipeline_rule	2021-04-23 13:01:28.906311+00
23	mimicINTapp	0005_job_infos	2021-04-23 13:01:29.055828+00
24	sessions	0001_initial	2021-04-23 13:01:29.181585+00
25	sites	0002_alter_domain_unique	2021-04-23 13:01:29.332551+00
\.


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 1, false);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
l4ri9vxxxvkpb7wgagzmxrtax13hkxsn	M2Q3OTJhZjE2ZTdiZDhmYWVlMzJiOGU3ZTcyZGVlYWZkYTU4NGFkMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1NDVhOWMxMjZjOTcxZjMyOTkyNTk2NDk1ZmI1MzhhYTA2NzczNTU2In0=	2024-03-15 11:45:03.137948+00
iuyksihyst92p00wxl7l5evixw0po4ha	M2Q3OTJhZjE2ZTdiZDhmYWVlMzJiOGU3ZTcyZGVlYWZkYTU4NGFkMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1NDVhOWMxMjZjOTcxZjMyOTkyNTk2NDk1ZmI1MzhhYTA2NzczNTU2In0=	2024-03-15 11:58:59.767362+00
939mxlhldht2kswv592ljef867pn7rgx	M2Q3OTJhZjE2ZTdiZDhmYWVlMzJiOGU3ZTcyZGVlYWZkYTU4NGFkMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1NDVhOWMxMjZjOTcxZjMyOTkyNTk2NDk1ZmI1MzhhYTA2NzczNTU2In0=	2024-03-29 13:00:29.827311+00
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public.django_site (id, domain, name) FROM stdin;
1	example.com	example.com
\.


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.django_site_id_seq', 1, false);


--
-- Data for Name: mimicINTapp_home_text; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public."mimicINTapp_home_text" ("text_ID", text_title, text_content) FROM stdin;
2	Tutorial	Go through a step-by-step guide to learn how to use mimicINTweb.
3	Run mimicINT	Submit your sequences (up to 50)
4	Jobs	Retrieve your predictions using a mimicINT job identifier. Results are kept for 7 days.
0	Presentation	mimicINTweb provides an easy-to-use interface to the mimicINT workflow to infer interactions between a set of microbial proteins of interest  and the human proteome, using known interaction templates (motif-domain and domain-domain).
5	News	Latest updates on mimicINT and mimicINTweb
6	Presentation	https://doi.org/10.1101/2022.11.04.515250 
1	Presentation	If you use mimicINTweb in your work, please do not forget to cite us! \r\n\r\nChoteau et al. (2022) mimicINT: a workflow for microbe-host protein interaction inference. bioRxiv, 
\.


--
-- Data for Name: mimicINTapp_job_infos; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public."mimicINTapp_job_infos" (job_id, email, submission_date, status, run_name, target_name, query_name, about) FROM stdin;
WChDko6h5GXXxkkvhWjr6T		2023-06-01 08:53:16.287434					
hBrH5iQYDuiYY4VjWLunLj		2023-06-01 09:00:27.430513					
hPcSkkoQxs8cGusHLoFWM5		2023-06-01 09:13:30.693381					
4PEQrUH9rjRnZZtTfx4esn		2023-06-01 09:17:55.998482					
mPj5AiswFznNQgcf2mUYDy		2023-06-01 12:16:11.438005					
7ybrK7eJNNjyHwNeawrZyd		2023-06-01 12:22:06.427889					
cg4TEogFXfAMFsMqQoSqBB		2023-06-01 12:25:05.76922					
XKsLzSJNgoQnHDSjcBWE7S		2023-06-01 12:26:56.384394					
83LgNRBiG6MAGEvfLvkrWV		2023-06-01 12:28:37.037677					
Ma5dq9YjPs5gdFCkmb3eug		2023-06-01 12:34:40.542425					
H5xyK8ZjgkRSur3wrMh4VZ		2023-06-01 12:40:14.772689					
KkZr3f9o3R7QpUuWSwdjuy		2023-06-01 12:45:50.591724					
MYVFWSRJuoFYBm2aj2esMZ		2023-06-01 13:20:50.156786					
SLkpDBoKmXw6jVcVdm3bz2		2023-06-01 13:25:48.938646					
FnhXn9Dovh3gGMeLiZ7sDv		2023-06-01 13:28:07.182671					
7gf6k4pxQE7uejkBqiiZQg		2023-06-01 13:29:34.07188					
fsKMxHqSo7kWxyxkhxGjvG		2023-06-01 13:32:22.410571					
finRRadzsdPUyrrj5BSHGX		2023-06-01 13:36:07.374446					
36jS9XFmSDnZ9UXjrZXsYG		2023-06-01 13:41:09.860626					
9AQk6TDHBrMbLPwAJsHyDq		2023-06-01 14:05:24.165897					
RuvH3y9WGRPHvqwypPuefN		2023-06-01 14:07:13.548032					
W5pGksqRTpdyQpaZtPgJNc		2023-06-02 08:42:19.051009					
eakzroFKxgytTKZDWVD8JY		2023-06-02 08:44:03.031176					
oVeDM9KpJ8Na8aGTgv2HWg		2023-06-02 08:44:29.577047					
eNAEyUH4umTwR9jE4cccGH		2023-06-02 08:47:36.172557					
QPBbj2D2eHQnCGzouajH99		2023-06-02 10:59:41.457343					
7NAibpCKR4pDNF8NGBsDsw		2023-06-09 12:07:13.009338					
3cMeuQLDx8tRf2T4dzB2fu		2023-06-09 12:14:10.21514					
FKroRdvHrSZPsH8cFuQJHg		2023-06-09 12:15:56.376982					
8N5nLSqmQu6JUWGjjTFu4R		2023-06-15 13:47:04.458753					
5JmGM9LVeTYZFVFPpZF2on		2023-06-26 09:37:37.417083					
CUJnqQfJC4tvhLpBLfi74z		2023-06-26 12:59:32.037864					
m7aBc5XsoHNvTVjpHTyioF		2023-06-29 11:11:42.938488					
dAByhrPTY3cmihVhhmA7Ki		2023-06-01 08:50:04.559807					
92boq9YyHQsUBVa2LBFzRs		2024-01-19 12:32:16.34867					
kyTcRCQygwkBmwb4ZaX6ny		2024-01-19 12:33:36.748846					
JcNqrUZ3ZVn9cKLLbWCe2q		2024-01-19 12:39:00.005718					
VyMAcSg3XPG8NiBc27Vaic		2024-01-19 12:46:58.186548					
SkQ5WJt5SaEWtSLb6oZUDx		2024-01-19 12:49:24.241965					
NBTZQ3meg7EgeUdwcNZe2a		2024-01-19 15:35:47.224103					
866ZBZyrfHdYiNgVE8dYy5		2024-01-19 16:35:24.950795					
CkorgJZBqpi7FwmwCTVifr		2024-01-31 10:39:36.077173					
ZxDvjBtfwVo6TqpTfwtHjQ		2024-02-05 15:22:47.962257					
c4BHzMzyQLcPsgDxaaQsui		2024-02-05 15:48:13.477386					
TQpbLonJGzoWejF3DdcGb6		2024-02-13 11:17:47.287442					
nGMEAKDRzPApM9xRK6twW6		2024-02-13 15:54:21.745647					
KQk4G9Tuq3k9qhJkpXbHd4		2024-02-13 16:15:19.576222					
DyT3UJr4qVfNtPBqR3SUPc		2024-02-13 17:22:51.062391					
B2H7KH7vctYdAMJWVAWRFE		2024-02-19 10:31:29.921257					
4n3TM2mrVYPtVTkeSMb7RL		2024-02-19 10:32:24.374717					
Z9gEVZMuMu5v4mExZvjRw2		2024-02-28 08:46:31.063705					
TbdsYYbWBLeRJ5c4pDMZ4R		2024-02-28 09:09:53.254232					
mWqSwM2f73VtrxCYDd6oK8		2024-02-28 15:03:26.567139					
KErQhdnqbEPDrhnYZe2XmG		2024-02-29 14:17:21.618252					
cYH2W5x3qmbiuVMkUBgXAB		2024-02-29 14:54:42.248956					
cv9vfh4pryLzsPik8P6FWo		2024-02-29 15:16:30.139084					
mU88aXEzqixRSPs7h4vkD6		2024-02-29 15:35:40.57476					
LmwawDDVsYNUBBhkWQzAw6		2024-03-01 12:15:55.175315					
E68hQyTChMVqMc4aXwRyet		2024-03-01 12:27:05.264672					
jH94ZMxS73VtSfrmLXzVTj		2024-03-01 12:38:33.683769					
83Wh6aJmeGqdeFBxdQ3oKa		2024-03-05 16:30:37.971828					
7sXa6C6eRQAEGYX5bxKwBt		2024-03-12 13:34:26.883673					
Gwn4CeMFtHvbUo8WuYiudA		2024-03-15 14:26:51.203867					
aweMSAmwoyQkTeRDTQDbiw		2024-03-15 14:58:50.934765					
juegM5G3TNZ4tasSTzKXem		2024-03-15 15:03:47.450924					
9UJA9qNZBGGRQ6JBGrQm9t		2024-03-15 15:30:44.5044					
ad7PG5D6dhpuLfn4tHEyLw		2024-03-15 15:47:56.113086					
kg5y5MKruUZWcRbmRCbdMm		2024-03-15 15:47:58.742719					
EDKathDH6gP7kVXAMpDw3C		2024-03-15 15:59:21.29014					
BxuW2As6QVEyEzHEewTTri		2024-03-19 10:41:16.02163					
DJfHEfJ2phPvCauyvndfJs		2024-03-19 10:55:38.536395					
gxVehATfdL6nBckERy34wW		2024-03-19 11:01:37.224572					
keQQFuMhvjmeJeCknzu36d		2024-03-19 12:02:36.893866					
XwYkV5FDVgpUXxFMGTrAMj		2024-03-19 12:28:41.701162					
\.


--
-- Data for Name: mimicINTapp_news_part; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public."mimicINTapp_news_part" ("news_ID", news_title, news_content) FROM stdin;
2	Update 2 - mimicINT domain score - October 20, 2023	We have implemented the mimciINT domain score also on micmiINTweb. You can now download a subset of the predicted interaction that fulfill the domain score filtering threshold.
1	Update 1 - mimicINTweb beta version online - September 1, 2023	First beta release of mimicINTweb is finally online for internal use.
3	Update 3 - put something here - January 1, 2024	put something here 
4	Update 4 - put something here	put something here
\.


--
-- Data for Name: mimicINTapp_output_file; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public."mimicINTapp_output_file" (file_accession, file_description, file_path, rule_id) FROM stdin;
query_seqnames_match_tsv	\N	/output/4_slim_detect/query_seqnames_match.tsv	match_query_sqce_names
query_slim_slimprob_tsv	\N	/output/4_slim_detect/query_slim_slimprob.tsv	aggregate_detect_slim_query_output
parsed_3did_txt	\N	/output/0_parse_3did/parsed_3did.txt	parse_3did
parsed_query_domain_interpro_tsv	\N	/output/3_detect_domain_query/parsed_query_domain_interpro.tsv	parse_domain_query
parsed_target_domain_interpro_tsv	\N	/output/2_detect_domain_target/parsed_target_domain_interpro.tsv	parse_domain_target
parsed_elm_classes_txt	\N	/output/1_parse_elm/parsed_elm_classes.txt	parse_elm
parsed_elm_summary_tsv	\N	/output/1_parse_elm/parsed_elm_summary.tsv	parse_elm
query_slim_slimprob_occ_tsv	\N	/output/4_slim_detect/query_slim_slimprob.occ.tsv	aggregate_detect_slim_query_output
iuscore	\N	/output/4_slim_detect/iuscore	aggregate_detect_slim_query_output
disorder_propensities_tsv	\N	/output/4_slim_detect/disorder_propensities.tsv	compute_query_disorder_propensity
query_domain_interpro_tsv	\N	/output/3_detect_domain_query/query_domain_interpro.tsv	detect_domain_query
target_domain_interpro_tsv	\N	/output/2_detect_domain_target/target_domain_interpro.tsv	detect_domain_target
query_1_slim_slimprob_tsv	\N	/output/4_slim_detect/1/query_1_slim_slimprob.tsv	detect_slim_query_1
iuscore_1	\N	/output/4_slim_detect/1/iuscore_1	detect_slim_query_1
SLiMProb_1	\N	/output/4_slim_detect/1/SLiMProb_1	detect_slim_query_1
query_1_slim_slimprob_occ_tsv	\N	/output/4_slim_detect/1/query_1_slim_slimprob.occ.tsv	detect_slim_query_1
generate_json_interaction_inference_all_interactions_json	\N	/output/5_interactions/all_interactions.json	generate_json_interaction_inference
query_proteins_features_json	\N	/output/6_summary/query_proteins_features.json	generate_json_query_features
inferred_all_interactions_tsv	\N	/output/5_interactions/inferred_all_interactions.tsv	interaction_inference
inferred_ddi_interactions_tsv	\N	/output/5_interactions/inferred_ddi_interactions.tsv	interaction_inference
inferred_dmi_interactions_tsv	\N	/output/5_interactions/inferred_dmi_interactions.tsv	interaction_inference
parsed_query_slim_slimprob_tsv	\N	/output/4_slim_detect/parsed_query_slim_slimprob.tsv	parse_slim_query
query_slims_tsv	\N	/output/7_renamed_sequences/query_slims.tsv	simplify_sequence_names
dd_interactions_tsv	\N	/output/7_renamed_sequences/dd_interactions.tsv	simplify_sequence_names
query_disorder_prop_tsv	\N	/output/7_renamed_sequences/query_disorder_prop.tsv	simplify_sequence_names
query_domains_tsv	\N	/output/7_renamed_sequences/query_domains.tsv	simplify_sequence_names
target_domains_tsv	\N	/output/7_renamed_sequences/target_domains.tsv	simplify_sequence_names
sequence_names_tsv	\N	/output/7_renamed_sequences/sequence_names.tsv	simplify_sequence_names
simplify_sequence_names_all_interactions_json	\N	/output/7_renamed_sequences/all_interactions.json	simplify_sequence_names
query_features_json	\N	/output/7_renamed_sequences/query_features.json	simplify_sequence_names
index_html	\N	/output/8_gprofiler/index.html	target_enrichment_gprofiler
all_interactions_tsv	\N	/output/7_renamed_sequences/all_interactions.tsv	simplify_sequence_names
dm_interactions_tsv	\N	/output/7_renamed_sequences/dm_interactions.tsv	simplify_sequence_names
4_splitted_query	\N	/output/4_splitted_query	split_query_dataset
unique_target_interactors_txt	\N	/output/8_gprofiler/unique_target_interactors.txt	target_enrichment_gprofiler
gprofiler_result_tsv	\N	/output/8_gprofiler/gprofiler_result.tsv	target_enrichment_gprofiler
unique_target_acc_txt	\N	/output/8_gprofiler/unique_target_acc.txt	target_enrichment_gprofiler
\.


--
-- Data for Name: mimicINTapp_pipeline_rule; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public."mimicINTapp_pipeline_rule" (rule_id, rule_order, rule_description, rule_duration, log_path) FROM stdin;
ddi_template_pfam_to_interpro	2	Convert the Pfam accessions in the file parsed from 3did into InterPro accessions	45	
parse_elm	3	Filter ELM classes based on their probability of occurence	30	
elm_domain_interactions_to_interpro	4	Convert the Pfam accessions in the ELM - domain interaction file into InterPro accessions	30	
simplify_sequence_names	17	Rename the sequences in all the output (optional rule)	300	
generate_json_query_features	18	Generate a json file that may be used to display the sequences on the web interface	60	
target_enrichment_gprofiler	19	Perform a gProfiler analysis on the target interactors	600	
detect_slim_query	8	Use SLiMProb (SLiM suite) to identify the SLiM in the query sequences, and optionally perfom a conservation analysis	150	
aggregate_detect_slim_query_output	9	Aggregate the outputs of the detect_slim_query rule into one single file	45	
parse_slim_query	11	Parse the output of SLiM Prob in order to get useful information	30	
compute_query_disorder_propensity	12	Compute the disordered propensity for query sequences	45	
interaction_inference	13	Inference the domain(target) - domain(query) and domain(target) - SLiM(query) interactions by combining the identifications of the domains and SLiM in the provided sequences and using H.\r\nsapiens known templates interaction	90	
parse_3did	1	Parse the flat file from 3did to gather domain-domain interaction templates	60	
get_target_prot_with_potential_interactions	5	\N	50	\N
detect_domain_query	6	Use InterProScan to detect the domains in the query sequences	330	
parse_domain_query	7	Parse the InterProScan output run on the query sequences to get useful information	30	
match_query_sqce_names	10	Compute the correspondences between the sequence names used by SLiMProb and the name of the sequence from the query fasta headers	15	
filter_dmi_on_domain_score	14	\N	50	\N
extract_binary_interactions	15	\N	50	\N
generate_json_interaction_inference	16	Generate a json file that may be used by Cytoscape	210	
\.


--
-- Data for Name: mimicINTapp_setting_prediction; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public."mimicINTapp_setting_prediction" ("setting_ID", setting_name, tooltip) FROM stdin;
11	Disorder Region (min.length)	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
0	Query Sequences	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
1	Run Name	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
2	Host Name	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
3	Microbe Species	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
4	About	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
5	Receive an email	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
6	Interaction Templates	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
7	Domain Family	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
8	Preferentially Targeted Network Modules	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
10	Disorder Threshold	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
12	Domain Detection Threshold	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
13	Conserved SLiM Only	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
9	Iumethod	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
14	Score_treshold_query	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
15	Simplify_seq_name	Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
\.


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_flatpage django_flatpage_pkey; Type: CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY public.django_flatpage
    ADD CONSTRAINT django_flatpage_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site django_site_domain_a2e37b91_uniq; Type: CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_domain_a2e37b91_uniq UNIQUE (domain);


--
-- Name: django_site django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: mimicINTapp_home_text mimicINTapp_home_text_pkey; Type: CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY public."mimicINTapp_home_text"
    ADD CONSTRAINT "mimicINTapp_home_text_pkey" PRIMARY KEY ("text_ID");


--
-- Name: mimicINTapp_job_infos mimicINTapp_job_infos_pkey; Type: CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY public."mimicINTapp_job_infos"
    ADD CONSTRAINT "mimicINTapp_job_infos_pkey" PRIMARY KEY (job_id);


--
-- Name: mimicINTapp_news_part mimicINTapp_news_part_pkey; Type: CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY public."mimicINTapp_news_part"
    ADD CONSTRAINT "mimicINTapp_news_part_pkey" PRIMARY KEY ("news_ID");


--
-- Name: mimicINTapp_output_file mimicINTapp_output_file_pkey; Type: CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY public."mimicINTapp_output_file"
    ADD CONSTRAINT "mimicINTapp_output_file_pkey" PRIMARY KEY (file_accession);


--
-- Name: mimicINTapp_pipeline_rule mimicINTapp_pipeline_rule_pkey; Type: CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY public."mimicINTapp_pipeline_rule"
    ADD CONSTRAINT "mimicINTapp_pipeline_rule_pkey" PRIMARY KEY (rule_id);


--
-- Name: mimicINTapp_setting_prediction mimicINTapp_setting_prediction_pkey; Type: CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY public."mimicINTapp_setting_prediction"
    ADD CONSTRAINT "mimicINTapp_setting_prediction_pkey" PRIMARY KEY ("setting_ID");


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: django
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: django
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: django
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: django
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: django
--

CREATE INDEX django_admin_log_417f1b1c ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: django
--

CREATE INDEX django_admin_log_e8701ad4 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_flatpage_url_41612362; Type: INDEX; Schema: public; Owner: django
--

CREATE INDEX django_flatpage_url_41612362 ON public.django_flatpage USING btree (url);


--
-- Name: django_flatpage_url_41612362_like; Type: INDEX; Schema: public; Owner: django
--

CREATE INDEX django_flatpage_url_41612362_like ON public.django_flatpage USING btree (url);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: django
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: django
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key);


--
-- Name: django_site_domain_a2e37b91_like; Type: INDEX; Schema: public; Owner: django
--

CREATE INDEX django_site_domain_a2e37b91_like ON public.django_site USING btree (domain);


--
-- Name: mimicINTapp_job_infos_job_id_9174fe91_like; Type: INDEX; Schema: public; Owner: django
--

CREATE INDEX "mimicINTapp_job_infos_job_id_9174fe91_like" ON public."mimicINTapp_job_infos" USING btree (job_id);


--
-- Name: mimicINTapp_output_file_file_accession_791f2553_like; Type: INDEX; Schema: public; Owner: django
--

CREATE INDEX "mimicINTapp_output_file_file_accession_791f2553_like" ON public."mimicINTapp_output_file" USING btree (file_accession);


--
-- Name: mimicINTapp_pipeline_rule_rule_ID_98e39e87_like; Type: INDEX; Schema: public; Owner: django
--

CREATE INDEX "mimicINTapp_pipeline_rule_rule_ID_98e39e87_like" ON public."mimicINTapp_pipeline_rule" USING btree (rule_id);


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_content_type_id_c4bce8eb_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_content_type_id_c4bce8eb_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: django
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

