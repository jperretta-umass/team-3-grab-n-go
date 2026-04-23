import { OrderItem } from "./OrderItem";

export class Order {
  dId : number;
  dormId : number;
  oId : number;
  uId : number;
  price : number;
  orderTime : string;
  items : OrderItem[]

  constructor(dId : number, dormId : number, oId : number, uId : number, price : number, orderTime : string, items : OrderItem[]) {
    this.dId = dId;
    this.dormId = dormId;
    this.oId = oId;
    this.uId = uId;
    this.price = price;
    this.orderTime = orderTime;
    this.items = items;
  }
}