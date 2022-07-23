with source_data_cast as (
    select *
    from {{ source('dwh_1', 'vehicles') }}
),
final as (
    select id,
        track_id,
        vehicle_type,
        cast(traveled_d as float) as traveled_d,
        avg_speed,
        lat,
        lon,
        speed,
        loan_acc,
        lat_acc,
        record_time
    from source_data_cast
)
SELECT *
FROM final