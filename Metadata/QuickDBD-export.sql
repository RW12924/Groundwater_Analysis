-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "Stations" (
    "_id" int  NOT NULL ,
    "site_code" text  NOT NULL ,
    "stn_id" text  NOT NULL ,
    "swn" text  NOT NULL ,
    "well_name" text  NOT NULL ,
    "continuous_data_station_number" text  NOT NULL ,
    "latitude" numeric  NOT NULL ,
    "longitude" numeric  NOT NULL ,
    "gse" numeric  NOT NULL ,
    "rpe" numeric  NOT NULL ,
    "gse_method" text  NOT NULL ,
    "gse_acc" text  NOT NULL ,
    "basin_code" text  NOT NULL ,
    "basin_name" text  NOT NULL ,
    "county_name" text  NOT NULL ,
    "well_depth" numeric  NOT NULL ,
    "well_use" text  NOT NULL ,
    "well_type" text  NOT NULL ,
    "wcr_no" text  NOT NULL ,
    "monitoring_program" text  NOT NULL ,
    CONSTRAINT "pk_Stations" PRIMARY KEY (
        "_id","site_code","stn_id"
    )
)

GO

CREATE TABLE "perforations" (
    "_id" int  NOT NULL ,
    "site_code" text  NOT NULL ,
    "top_prf_int" numeric  NOT NULL ,
    "bot_prf_int" numeric  NOT NULL ,
    CONSTRAINT "pk_perforations" PRIMARY KEY (
        "_id"
    )
)

GO

CREATE TABLE "measurements" (
    "_id" int  NOT NULL ,
    "site_code" text  NOT NULL ,
    "msmt_date" timestamp  NOT NULL ,
    "wlm_rpe" numeric  NOT NULL ,
    "wlm_gse" numeric  NOT NULL ,
    "gwe" numeric  NOT NULL ,
    "gse_gwe" numeric  NOT NULL ,
    "wlm_qa_desc" text  NOT NULL ,
    "wlm_qa_detail" text  NOT NULL ,
    "wlm_mthd_desc" text  NOT NULL ,
    "wlm_acc_desc" text  NOT NULL ,
    "wlm_org_name" text  NOT NULL ,
    "coop_org_name" text  NOT NULL ,
    "monitoring_program" text  NOT NULL ,
    "source" text  NOT NULL ,
    "msmt_cmt" text  NOT NULL ,
    CONSTRAINT "pk_measurements" PRIMARY KEY (
        "_id"
    )
)

GO

ALTER TABLE "perforations" ADD CONSTRAINT "fk_perforations_site_code" FOREIGN KEY("site_code")
REFERENCES "Stations" ("site_code")
GO

ALTER TABLE "measurements" ADD CONSTRAINT "fk_measurements_site_code" FOREIGN KEY("site_code")
REFERENCES "Stations" ("site_code")
GO

