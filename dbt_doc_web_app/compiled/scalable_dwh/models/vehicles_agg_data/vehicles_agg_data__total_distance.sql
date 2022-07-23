with source_data as (
    select *
    from "dwh_1"."public"."vehicles_cast_feature"
),
final as (
    select 
    vehicle_type,
    SUM(traveled_d)
    from vehicles_cast_feature
    group by
    vehicle_type 

)
SELECT *
FROM final