import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { CustomerAPI, CustomercreateAPI, CustomerstatusAPI, ProductAPI, OrdercreateAPI, OrderitemAPI } from "./api";
import * as types from "./types";


export const useGetCustomers = () => {
  return useQuery({
    queryKey: ["customers"],
    queryFn: CustomerAPI.getAll,
  });
};

export const useGetCustomer = (id: number) => {
  return useQuery({
    queryKey: ["customers", id],
    queryFn: () => CustomerAPI.getById(id),
    enabled: !!id,
  });
};

export const useCreateCustomer = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: types.CustomerCreate) => CustomerAPI.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["customers"] });
    },
  });
};

export const useUpdateCustomer = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: types.CustomerUpdate }) => CustomerAPI.update(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["customers"] });
      queryClient.invalidateQueries({ queryKey: ["customers", variables.id] });
    },
  });
};

export const useDeleteCustomer = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => CustomerAPI.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["customers"] });
    },
  });
};

export const useGetCustomercreates = () => {
  return useQuery({
    queryKey: ["customercreates"],
    queryFn: CustomercreateAPI.getAll,
  });
};

export const useGetCustomercreate = (id: number) => {
  return useQuery({
    queryKey: ["customercreates", id],
    queryFn: () => CustomercreateAPI.getById(id),
    enabled: !!id,
  });
};

export const useCreateCustomercreate = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: types.CustomercreateCreate) => CustomercreateAPI.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["customercreates"] });
    },
  });
};

export const useUpdateCustomercreate = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: types.CustomercreateUpdate }) => CustomercreateAPI.update(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["customercreates"] });
      queryClient.invalidateQueries({ queryKey: ["customercreates", variables.id] });
    },
  });
};

export const useDeleteCustomercreate = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => CustomercreateAPI.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["customercreates"] });
    },
  });
};

export const useGetCustomerstatuss = () => {
  return useQuery({
    queryKey: ["customerstatuss"],
    queryFn: CustomerstatusAPI.getAll,
  });
};

export const useGetCustomerstatus = (id: number) => {
  return useQuery({
    queryKey: ["customerstatuss", id],
    queryFn: () => CustomerstatusAPI.getById(id),
    enabled: !!id,
  });
};

export const useCreateCustomerstatus = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: types.CustomerstatusCreate) => CustomerstatusAPI.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["customerstatuss"] });
    },
  });
};

export const useUpdateCustomerstatus = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: types.CustomerstatusUpdate }) => CustomerstatusAPI.update(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["customerstatuss"] });
      queryClient.invalidateQueries({ queryKey: ["customerstatuss", variables.id] });
    },
  });
};

export const useDeleteCustomerstatus = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => CustomerstatusAPI.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["customerstatuss"] });
    },
  });
};

export const useGetProducts = () => {
  return useQuery({
    queryKey: ["products"],
    queryFn: ProductAPI.getAll,
  });
};

export const useGetProduct = (id: number) => {
  return useQuery({
    queryKey: ["products", id],
    queryFn: () => ProductAPI.getById(id),
    enabled: !!id,
  });
};

export const useCreateProduct = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: types.ProductCreate) => ProductAPI.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["products"] });
    },
  });
};

export const useUpdateProduct = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: types.ProductUpdate }) => ProductAPI.update(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["products"] });
      queryClient.invalidateQueries({ queryKey: ["products", variables.id] });
    },
  });
};

export const useDeleteProduct = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => ProductAPI.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["products"] });
    },
  });
};

export const useGetOrdercreates = () => {
  return useQuery({
    queryKey: ["ordercreates"],
    queryFn: OrdercreateAPI.getAll,
  });
};

export const useGetOrdercreate = (id: number) => {
  return useQuery({
    queryKey: ["ordercreates", id],
    queryFn: () => OrdercreateAPI.getById(id),
    enabled: !!id,
  });
};

export const useCreateOrdercreate = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: types.OrdercreateCreate) => OrdercreateAPI.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["ordercreates"] });
    },
  });
};

export const useUpdateOrdercreate = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: types.OrdercreateUpdate }) => OrdercreateAPI.update(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["ordercreates"] });
      queryClient.invalidateQueries({ queryKey: ["ordercreates", variables.id] });
    },
  });
};

export const useDeleteOrdercreate = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => OrdercreateAPI.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["ordercreates"] });
    },
  });
};

export const useGetOrderitems = () => {
  return useQuery({
    queryKey: ["orderitems"],
    queryFn: OrderitemAPI.getAll,
  });
};

export const useGetOrderitem = (id: number) => {
  return useQuery({
    queryKey: ["orderitems", id],
    queryFn: () => OrderitemAPI.getById(id),
    enabled: !!id,
  });
};

export const useCreateOrderitem = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: types.OrderitemCreate) => OrderitemAPI.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["orderitems"] });
    },
  });
};

export const useUpdateOrderitem = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: types.OrderitemUpdate }) => OrderitemAPI.update(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["orderitems"] });
      queryClient.invalidateQueries({ queryKey: ["orderitems", variables.id] });
    },
  });
};

export const useDeleteOrderitem = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => OrderitemAPI.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["orderitems"] });
    },
  });
};
