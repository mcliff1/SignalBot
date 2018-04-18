
CREATE TABLE public.soil_bot (
    id bigint NOT NULL,
    version bigint,
    created_at timestamp without time zone,
    created_by character varying(20),
    updated_at timestamp without time zone,
    updated_by character varying(20),
    battery real NOT NULL,
    botid bigint,
    bot_type bigint,
    humidity real NOT NULL,
    soilmoisture1 real NOT NULL,
    soilmoisture2 real NOT NULL,
    soilmoisture3 real NOT NULL,
    tempc real NOT NULL,
    tempf real NOT NULL,
    volts real NOT NULL,
    deviceid character varying(255),
    sensor_number integer
);




CREATE SEQUENCE public.soil_bot_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.soil_bot_id_seq OWNED BY public.soil_bot.id;
ALTER TABLE ONLY public.soil_bot ALTER COLUMN id SET DEFAULT nextval('public.soil_bot_id_seq'::regclass);
ALTER TABLE ONLY public.soil_bot
    ADD CONSTRAINT soil_bot_pkey PRIMARY KEY (id);








CREATE TABLE public.cure_bot (
    id bigint NOT NULL,
    version bigint,
    created_at timestamp without time zone,
    created_by character varying(20),
    updated_at timestamp without time zone,
    updated_by character varying(20),
    battery real NOT NULL,
    infrared real NOT NULL,
    tempc real NOT NULL,
    tempf real NOT NULL,
    uvindex real NOT NULL,
    visible real NOT NULL,
    volts real NOT NULL,
    humidity real NOT NULL,
    deviceid character varying(255)
);


CREATE SEQUENCE public.cure_bot_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cure_bot_id_seq OWNED BY public.cure_bot.id;
ALTER TABLE ONLY public.cure_bot ALTER COLUMN id SET DEFAULT nextval('public.cure_bot_id_seq'::regclass);
ALTER TABLE ONLY public.cure_bot
    ADD CONSTRAINT cure_bot_pkey PRIMARY KEY (id);






CREATE TABLE public.gas_bot (
    id bigint NOT NULL,
    version bigint,
    battery real NOT NULL,
    created_at timestamp without time zone,
    created_by character varying(20),
    deviceid character varying(255),
    updated_at timestamp without time zone,
    updated_by character varying(20),
    volts real NOT NULL,
    carbondioxide real NOT NULL
);



CREATE SEQUENCE public.gas_bot_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gas_bot_id_seq OWNED BY public.gas_bot.id;
ALTER TABLE ONLY public.gas_bot ALTER COLUMN id SET DEFAULT nextval('public.gas_bot_id_seq'::regclass);
ALTER TABLE ONLY public.gas_bot
    ADD CONSTRAINT gas_bot_pkey PRIMARY KEY (id);






















CREATE TABLE public.light_bot (
    id bigint NOT NULL,
    version bigint,
    created_at timestamp without time zone,
    created_by character varying(20),
    updated_at timestamp without time zone,
    updated_by character varying(20),
    battery real NOT NULL,
    botid bigint,
    bot_type bigint,
    humidity real NOT NULL,
    lux real NOT NULL,
    par real NOT NULL,
    tempc real NOT NULL,
    tempf real NOT NULL,
    volts real NOT NULL,
    fullspec real NOT NULL,
    infrared real NOT NULL,
    visible real NOT NULL,
    deviceid character varying(255)
);
CREATE SEQUENCE public.light_bot_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.light_bot_id_seq OWNED BY public.light_bot.id;
ALTER TABLE ONLY public.light_bot ALTER COLUMN id SET DEFAULT nextval('public.light_bot_id_seq'::regclass);
ALTER TABLE ONLY public.light_bot
    ADD CONSTRAINT light_bot_pkey PRIMARY KEY (id);







CREATE TABLE public.aqua_bot (
    id bigint NOT NULL,
    version bigint,
    created_at timestamp without time zone,
    created_by character varying(20),
    updated_at timestamp without time zone,
    deviceid character varying(255),
    ec real NOT NULL,
    sal real NOT NULL,
    sg real NOT NULL,
    tds real NOT NULL,
    tempc real NOT NULL,
    battery real,
    ph real,
    doxygen real,
    tempf real,
    volts real,
    updated_by character varying(20)
);
CREATE SEQUENCE public.aqua_bot_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.aqua_bot_id_seq OWNED BY public.aqua_bot.id;
ALTER TABLE ONLY public.aqua_bot ALTER COLUMN id SET DEFAULT nextval('public.aqua_bot_id_seq'::regclass);
ALTER TABLE ONLY public.aqua_bot
    ADD CONSTRAINT aqua_bot_pkey PRIMARY KEY (id);

