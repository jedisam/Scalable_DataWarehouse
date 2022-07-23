with source_data as (
    select *
    from "dwh_1"."public"."vehicles_cast_feature"
),
final as (
    select vehicle_type,
        COUNT(*)
    from source_data
    group by vehicle_type
)
SELECT *
FROM final