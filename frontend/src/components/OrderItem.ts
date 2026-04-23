export class OrderItem {
    order_id : number;
    menu_item_id : number;
    quantity : number;

    constructor(order_id : number, menu_item_id : number, quantity : number){
        this.order_id = order_id;
        this.menu_item_id = menu_item_id;
        this.quantity = quantity;
    }
}