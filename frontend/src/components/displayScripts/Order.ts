export class Order {
  dId : number;
  dormId : number;
  oId : number;
  uId : number;
  price : number;
  orderTime : string;
  mainId : number[];
  sideId : number[];
  specialInstructions : string = "None";
  deliveryInstructions : string = "None";

  constructor(dId : number, dormId : number, oId : number, uId : number, price : number, orderTime : string, mainId : number[], sideId : number[], specialInstructions : string = "None", deliveryInstructions : string = "None") {
    this.dId = dId;
    this.dormId = dormId;
    this.oId = oId;
    this.uId = uId;
    this.price = price;
    this.orderTime = orderTime;
    this.mainId = mainId;
    this.sideId = sideId;
    this.specialInstructions = specialInstructions;
    this.deliveryInstructions = deliveryInstructions;
  }
}