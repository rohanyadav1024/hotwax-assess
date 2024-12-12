from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, models
from ..database import get_db
from ..oauth import get_current_user

router = APIRouter(prefix='/orders', tags=["Orders"])

@router.post('', status_code=status.HTTP_201_CREATED)
def create_order(request: schemas.Order, db: Session = Depends(get_db)):
    new_order = models.Order_Header(
        order_date=request.order_date,
        customer_id=request.customer_id,
        shipping_contact_mech_id=request.shipping_contact_mech_id,
        billing_contact_mech_id=request.billing_contact_mech_id)

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in request.order_items:
        new_order_item = models.Order_Items(
            quantity=item.quantity,
            status=item.status,
            product_id=item.product_id,
            order_id=new_order.order_id
        )
        db.add(new_order_item)
        # new_order.Order_Header.append(new_order_item)

    db.commit()
    db.refresh(new_order)

    return {
        "message": "Order created successfully",
        "order_id": new_order.order_id,
        "order_date": new_order.order_date,
        "customer_id": new_order.customer_id,
        "shipping_contact_mech_id": new_order.shipping_contact_mech_id,
        "billing_contact_mech_id": new_order.billing_contact_mech_id,
        "order_items": new_order.Order_Items
    }

@router.get('/{order_id}', status_code=status.HTTP_201_CREATED)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order_Header).filter(models.Order_Header.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {order_id} not found")
    return {
        "order_id": order.order_id,
        "order_date": order.order_date,
        "customer_id": order.customer_id,
        "shipping_contact_mech_id": order.shipping_contact_mech_id,
        "billing_contact_mech_id": order.billing_contact_mech_id,
        "order_items": order.Order_Items
    }

# @router.put('/{order_id}', status_code=status.HTTP_201_CREATED)
# def update_order(order_id: int, request: schemas.Order, db: Session = Depends(get_db)):
#     existing_order = db.query(models.Order_Header).filter(models.Order_Header.order_id == order_id).first()
#     if not existing_order:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {order_id} not found")
    
#     existing_order.order_date = request.order_date
#     existing_order.customer_id = request.customer_id
#     existing_order.shipping_contact_mech_id = request.shipping_contact_mech_id
#     existing_order.billing_contact_mech_id = request.billing_contact_mech_id

#     db.commit()
#     db.refresh(existing_order)

#     return {
#         "message": "Order updated successfully",
#         "order_id": existing_order.order_id,
#         "order_date": existing_order.order_date,
#         "customer_id": existing_order.customer_id,
#         "shipping_contact_mech_id": existing_order.shipping_contact_mech_id,
#         "billing_contact_mech_id": existing_order.billing_contact_mech_id,
#         "order_items": existing_order.Order_Items
#     }


@router.put('/{order_id}', status_code=status.HTTP_201_CREATED)
def update_order(order_id: int, request: schemas.UpdateOrder, db: Session = Depends(get_db)):
    existing_order = db.query(models.Order_Header).filter(models.Order_Header.order_id == order_id).first()
    if not existing_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {order_id} not found")


    # update details if provided for shipping_contact_mech table and billing_contact_mech in Contact_Mech table
    if request.shipping_id:
        existing_order.shipping_contact_mech_id = request.shipping_id
    else:
        shipping_contact_mech = db.query(models.ContactMech).filter(models.ContactMech.contact_mech_id == existing_order.shipping_contact_mech_id).first()
        if not shipping_contact_mech:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shipping contact with provided id {existing_order.shipping_contact_mech_id} not found")

        if request.shipping_details.street_address:
            shipping_contact_mech.street_address = request.shipping_details.street_address
        if request.shipping_details.country:
            shipping_contact_mech.country = request.shipping_details.country
        if request.shipping_details.state:
            shipping_contact_mech.state = request.shipping_details.state
        if request.shipping_details.postal_code:
            shipping_contact_mech.postal_code = request.shipping_details.postal_code
        if request.shipping_details.phone_number:
            shipping_contact_mech.phone_number = request.shipping_details.phone_number

    if request.billing_id is not None:
        existing_order.billing_contact_mech_id = request.billing_id
    else:
        billing_contact_mech = db.query(models.ContactMech).filter(models.ContactMech.contact_mech_id == existing_order.billing_contact_mech_id).first()
        if not billing_contact_mech:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Billing contact with provided id {existing_order.billing_contact_mech_id} not found")
        if request.billing_details.street_address:
            billing_contact_mech.street_address = request.billing_details.street_address
        if request.billing_details.country:
            billing_contact_mech.country = request.billing_details.country
        if request.billing_details.state:
            billing_contact_mech.state = request.billing_details.state
        if request.billing_details.postal_code:
            billing_contact_mech.postal_code = request.billing_details.postal_code
        if request.billing_details.phone_number:
            billing_contact_mech.phone_number = request.billing_details.phone_number

    db.commit()
    db.refresh(existing_order)

    shipping_contact_mech = db.query(models.ContactMech).filter(models.ContactMech.contact_mech_id == existing_order.shipping_contact_mech_id).first()
    billing_contact_mech = db.query(models.ContactMech).filter(models.ContactMech.contact_mech_id == existing_order.billing_contact_mech_id).first()

    return {
        "message": "Order updated successfully",
        "order_id": existing_order.order_id,
        "order_date": existing_order.order_date,
        "customer_id": existing_order.customer_id,
        "shipping_contact_mech": shipping_contact_mech,
        "billing_contact_mech": billing_contact_mech,
        "order_items": existing_order.Order_Items
    }

@router.delete('/{order_id}', status_code=status.HTTP_201_CREATED)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order_Header).filter(models.Order_Header.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {order_id} not found")

    db.delete(order)
    db.commit()

    return {
        "message": "Order deleted successfully"
    }


# For Order Items

@router.post('/{order_id}/items', status_code=status.HTTP_201_CREATED)
def create_order_item(order_id: int, request: schemas.OrderItem, db: Session = Depends(get_db)):
    order = db.query(models.Order_Header).filter(models.Order_Header.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {order_id} not found")
    
    new_order_item = models.Order_Items(
        quantity=request.quantity,
        status=request.status,
        product_id=request.product_id,
        order_id=order_id
    )

    db.add(new_order_item)
    db.commit()
    db.refresh(new_order_item)

    return {
        "message": "Order item updated successfully",
        "order_item_seq_id": new_order_item.order_item_seq_id,
        "quantity": new_order_item.quantity,
        "status": new_order_item.status,
        "product_id": new_order_item.product_id,
        "order_id": new_order_item.order_id
    }

@router.put('/{order_id}/items/{order_item_seq_id}', status_code=status.HTTP_201_CREATED)
def update_order_item(order_id: int, order_item_seq_id: int, request : schemas.UpdateOrderItem, db: Session = Depends(get_db)):
    order_item = db.query(models.Order_Items).filter(models.Order_Items.order_id == order_id, models.Order_Items.order_item_seq_id == order_item_seq_id).first()

    if not order_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order item with id {order_item_seq_id} not found")
    
    if request.quantity:
        order_item.quantity = request.quantity
    if request.status:
        order_item.status = request.status

    db.commit()
    db.refresh(order_item)

    return {
        "message": "Order item updated successfully",
        "order_item_seq_id": order_item.order_item_seq_id,
        "quantity": order_item.quantity,
        "status": order_item.status,
        "product_id": order_item.product_id,
        "order_id": order_item.order_id
    }


@router.delete('/{order_id}/items/{order_item_seq_id}', status_code=status.HTTP_201_CREATED)
def delete_order_item(order_id: int, order_item_seq_id: int, db: Session = Depends(get_db)):
    order_item = db.query(models.Order_Items).filter(models.Order_Items.order_id == order_id, models.Order_Items.order_item_seq_id == order_item_seq_id).first()
    if not order_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order item with id {order_item_seq_id} not found")
    
    db.delete(order_item)
    db.commit()

    return {
        "message": "Order item deleted successfully"
    }