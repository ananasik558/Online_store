CREATE OR REPLACE FUNCTION add_deal_on_new_client()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM client WHERE id = NEW.id) THEN                                           
        UPDATE car
        SET count = count - 1 
        WHERE id=(SELECT id FROM car WHERE model=NEW.car_model LIMIT 1);
            
        INSERT INTO deal (client_id, id, car, created_at)
        VALUES (NEW.id, uuid_generate_v4(), NEW.car_model, Now());
            
        RETURN NEW;
            
    END IF;
END;
$$                
LANGUAGE plpgsql;