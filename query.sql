select last_name,first_name,result.number_ren, postal_code, lat, lon
from customer,
     address,
     (select customer_id, count(*) as number_ren
      from rental
      group by customer_id
      having number_ren = (select max(a.number_ren)
                           from (select customer_id, count(*) as number_ren
                                 from rental
                                 group by customer_id) a)) as result
where result.customer_id = customer.customer_id
and customer.address_id = address.address_id