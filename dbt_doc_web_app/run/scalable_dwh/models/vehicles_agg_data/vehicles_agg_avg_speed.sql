
  create view "dwh_1"."public"."vehicles_agg_avg_speed__dbt_tmp" as (
    with source_data as (
    select *
    from "dwh_1"."public"."vehicles_cast_feature"
),
final as (
    select vehicle_type,
        AVG(avg_speed)
    from source_data
    group by vehicle_type
)
SELECT *
FROM final
  );