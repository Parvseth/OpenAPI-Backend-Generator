// Auto-generated TypeScript types from OpenAPI Schema


export interface Customer {

  id: number;

  name: string;

  email: string;

  status: string;

}

export interface CustomerCreate {




  name: string;



  email: string;



  status: string;


}

export interface CustomerUpdate {




  name?: string;



  email?: string;



  status?: string;


}

export interface Customercreate {

  id: number;

  name: string;

  email: string;

}

export interface CustomercreateCreate {




  name: string;



  email: string;


}

export interface CustomercreateUpdate {




  name?: string;



  email?: string;


}

export interface Customerstatus {

  id: number;

}

export interface CustomerstatusCreate {



}

export interface CustomerstatusUpdate {



}

export interface Product {

  id: number;

  name: string;

  price: number;

}

export interface ProductCreate {




  name: string;



  price: number;


}

export interface ProductUpdate {




  name?: string;



  price?: number;


}

export interface Ordercreate {

  id: number;

  customer_id: number;

  items: string;

}

export interface OrdercreateCreate {




  customer_id: number;



  items: string;


}

export interface OrdercreateUpdate {




  customer_id?: number;



  items?: string;


}

export interface Orderitem {

  id: number;

  product_id: number;

  quantity: number;

}

export interface OrderitemCreate {




  product_id: number;



  quantity: number;


}

export interface OrderitemUpdate {




  product_id?: number;



  quantity?: number;


}
