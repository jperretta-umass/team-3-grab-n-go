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

// make the data reactive

// create a order item object (for frontend)

// Create a convert function that turns JSON data into order object

// Create fetch function
//   - converts the data into order object

// Update values using computed() onto the UI 
