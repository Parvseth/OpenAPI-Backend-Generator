import axios from "axios";
import * as types from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});


export const CustomerAPI = {
  getAll: async () => {
    const response = await apiClient.get<types.Customer[]>(`/customers`);
    return response.data;
  },
  getById: async (id: number) => {
    const response = await apiClient.get<types.Customer>(`/customers/${id}`);
    return response.data;
  },
  create: async (data: types.CustomerCreate) => {
    const response = await apiClient.post<types.Customer>(`/customers`, data);
    return response.data;
  },
  update: async (id: number, data: types.CustomerUpdate) => {
    const response = await apiClient.put<types.Customer>(`/customers/${id}`, data);
    return response.data;
  },
  delete: async (id: number) => {
    const response = await apiClient.delete(`/customers/${id}`);
    return response.data;
  },
};

export const CustomercreateAPI = {
  getAll: async () => {
    const response = await apiClient.get<types.Customercreate[]>(`/customercreates`);
    return response.data;
  },
  getById: async (id: number) => {
    const response = await apiClient.get<types.Customercreate>(`/customercreates/${id}`);
    return response.data;
  },
  create: async (data: types.CustomercreateCreate) => {
    const response = await apiClient.post<types.Customercreate>(`/customercreates`, data);
    return response.data;
  },
  update: async (id: number, data: types.CustomercreateUpdate) => {
    const response = await apiClient.put<types.Customercreate>(`/customercreates/${id}`, data);
    return response.data;
  },
  delete: async (id: number) => {
    const response = await apiClient.delete(`/customercreates/${id}`);
    return response.data;
  },
};

export const CustomerstatusAPI = {
  getAll: async () => {
    const response = await apiClient.get<types.Customerstatus[]>(`/customerstatuss`);
    return response.data;
  },
  getById: async (id: number) => {
    const response = await apiClient.get<types.Customerstatus>(`/customerstatuss/${id}`);
    return response.data;
  },
  create: async (data: types.CustomerstatusCreate) => {
    const response = await apiClient.post<types.Customerstatus>(`/customerstatuss`, data);
    return response.data;
  },
  update: async (id: number, data: types.CustomerstatusUpdate) => {
    const response = await apiClient.put<types.Customerstatus>(`/customerstatuss/${id}`, data);
    return response.data;
  },
  delete: async (id: number) => {
    const response = await apiClient.delete(`/customerstatuss/${id}`);
    return response.data;
  },
};

export const ProductAPI = {
  getAll: async () => {
    const response = await apiClient.get<types.Product[]>(`/products`);
    return response.data;
  },
  getById: async (id: number) => {
    const response = await apiClient.get<types.Product>(`/products/${id}`);
    return response.data;
  },
  create: async (data: types.ProductCreate) => {
    const response = await apiClient.post<types.Product>(`/products`, data);
    return response.data;
  },
  update: async (id: number, data: types.ProductUpdate) => {
    const response = await apiClient.put<types.Product>(`/products/${id}`, data);
    return response.data;
  },
  delete: async (id: number) => {
    const response = await apiClient.delete(`/products/${id}`);
    return response.data;
  },
};

export const OrdercreateAPI = {
  getAll: async () => {
    const response = await apiClient.get<types.Ordercreate[]>(`/ordercreates`);
    return response.data;
  },
  getById: async (id: number) => {
    const response = await apiClient.get<types.Ordercreate>(`/ordercreates/${id}`);
    return response.data;
  },
  create: async (data: types.OrdercreateCreate) => {
    const response = await apiClient.post<types.Ordercreate>(`/ordercreates`, data);
    return response.data;
  },
  update: async (id: number, data: types.OrdercreateUpdate) => {
    const response = await apiClient.put<types.Ordercreate>(`/ordercreates/${id}`, data);
    return response.data;
  },
  delete: async (id: number) => {
    const response = await apiClient.delete(`/ordercreates/${id}`);
    return response.data;
  },
};

export const OrderitemAPI = {
  getAll: async () => {
    const response = await apiClient.get<types.Orderitem[]>(`/orderitems`);
    return response.data;
  },
  getById: async (id: number) => {
    const response = await apiClient.get<types.Orderitem>(`/orderitems/${id}`);
    return response.data;
  },
  create: async (data: types.OrderitemCreate) => {
    const response = await apiClient.post<types.Orderitem>(`/orderitems`, data);
    return response.data;
  },
  update: async (id: number, data: types.OrderitemUpdate) => {
    const response = await apiClient.put<types.Orderitem>(`/orderitems/${id}`, data);
    return response.data;
  },
  delete: async (id: number) => {
    const response = await apiClient.delete(`/orderitems/${id}`);
    return response.data;
  },
};
