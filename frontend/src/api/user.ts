import request from '@/utils/request'
import type { User, Role, Permission, Department, PageResult } from '@/types'

export const userApi = {
  getUsers(params?: { skip?: number; limit?: number }) {
    return request.get<User[]>('/users/', { params })
  },
  
  getUser(id: number) {
    return request.get<User>(`/users/${id}`)
  },
  
  createUser(data: any) {
    return request.post<User>('/users/', data)
  },
  
  updateUser(id: number, data: any) {
    return request.put<User>(`/users/${id}`, data)
  },
  
  deleteUser(id: number) {
    return request.delete(`/users/${id}`)
  },
  
  assignRoles(userId: number, data: { role_ids: number[] }) {
    return request.post(`/users/${userId}/roles`, data)
  },
  
  getRoles() {
    return request.get<Role[]>('/users/roles/')
  },
  
  createRole(data: any) {
    return request.post<Role>('/users/roles/', data)
  },
  
  updateRole(id: number, data: any) {
    return request.put<Role>(`/users/roles/${id}`, data)
  },
  
  deleteRole(id: number) {
    return request.delete(`/users/roles/${id}`)
  },
  
  assignPermissions(roleId: number, data: { permission_ids: number[] }) {
    return request.post(`/users/roles/${roleId}/permissions`, data)
  },
  
  getPermissions() {
    return request.get<Permission[]>('/users/permissions/')
  },
  
  createPermission(data: any) {
    return request.post<Permission>('/users/permissions/', data)
  }
}

export const departmentApi = {
  getDepartments(params?: { skip?: number; limit?: number }) {
    return request.get<Department[]>('/departments/', { params })
  },
  
  getDepartmentTree() {
    return request.get<Department[]>('/departments/tree')
  },
  
  getDepartment(id: number) {
    return request.get<Department>(`/departments/${id}`)
  },
  
  createDepartment(data: any) {
    return request.post<Department>('/departments/', data)
  },
  
  updateDepartment(id: number, data: any) {
    return request.put<Department>(`/departments/${id}`, data)
  },
  
  deleteDepartment(id: number) {
    return request.delete(`/departments/${id}`)
  }
}
