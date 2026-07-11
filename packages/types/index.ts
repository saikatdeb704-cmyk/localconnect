// User Types
export interface User {
  id: string;
  name: string;
  email: string;
  phone: string;
  avatar?: string;
  role: 'resident' | 'shopkeeper' | 'service_provider' | 'admin';
  locality_id: string;
  created_at: string;
  updated_at: string;
}

// Locality Types
export interface Locality {
  id: string;
  name: string;
  city: string;
  state: string;
  pincode: string;
  lat: number;
  lng: number;
}

// Post Types
export interface Post {
  id: string;
  user_id: string;
  caption: string;
  image?: string;
  video?: string;
  category: 'lost_found' | 'event' | 'blood_request' | 'emergency' | 'update' | 'photo' | 'video' | 'poll';
  likes_count: number;
  comments_count: number;
  created_at: string;
  user?: User;
}

// Shop Types
export interface Shop {
  id: string;
  owner_id: string;
  name: string;
  category: string;
  description?: string;
  image?: string;
  location: {
    lat: number;
    lng: number;
  };
  phone: string;
  address: string;
  locality_id: string;
}

// Product Types
export interface Product {
  id: string;
  shop_id: string;
  name: string;
  price: number;
  stock: number;
  image?: string;
  description?: string;
}

// Order Types
export interface Order {
  id: string;
  buyer_id: string;
  shop_id: string;
  status: 'pending' | 'confirmed' | 'packed' | 'shipped' | 'delivered' | 'cancelled';
  amount: number;
  items: OrderItem[];
  created_at: string;
  updated_at: string;
}

export interface OrderItem {
  product_id: string;
  quantity: number;
  price: number;
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}
