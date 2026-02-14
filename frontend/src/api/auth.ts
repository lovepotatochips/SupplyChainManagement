// 导入HTTP请求工具
import request from '@/utils/request'
// 导入类型定义
import type { User, ApiResponse } from '@/types'

/**
 * 登录请求数据接口
 */
export interface LoginData {
  username: string  // 用户名
  password: string  // 密码
}

/**
 * 注册请求数据接口
 */
export interface RegisterData {
  username: string         // 用户名
  password: string         // 密码
  real_name?: string       // 真实姓名（可选）
  email?: string           // 邮箱（可选）
  phone?: string           // 手机号（可选）
  department_id?: number   // 部门ID（可选）
}

/**
 * 认证相关API
 */
export const authApi = {
  /**
   * 用户登录
   * @param data 登录数据（用户名和密码）
   * @returns Promise包含access_token和token_type
   */
  login(data: LoginData) {
    // 使用URLSearchParams构建表单数据
    const formData = new URLSearchParams()
    formData.append('username', data.username)
    formData.append('password', data.password)
    return request.post<{ access_token: string; token_type: string }>('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
  },
  
  /**
   * 演示模式登录
   * @param data 登录数据
   * @returns 模拟的登录响应，包含生成的token
   */
  loginDemo(data: LoginData) {
    return new Promise<{ access_token: string; token_type: string }>((resolve) => {
      setTimeout(() => {
        resolve({
          access_token: 'demo-token-' + Date.now(),
          token_type: 'bearer'
        })
      }, 500)
    })
  },
  
  /**
   * 用户注册
   * @param data 注册数据
   * @returns 注册成功的用户信息
   */
  register(data: RegisterData) {
    return request.post<User>('/auth/register', data)
  },
  
  /**
   * 获取当前登录用户信息
   * @returns 当前用户的详细信息
   */
  getCurrentUser() {
    return request.get<User>('/auth/me')
  },
  
  /**
   * 演示模式获取当前用户信息
   * @param username 用户名
   * @returns 模拟的用户信息
   */
  getCurrentUserDemo(username: string) {
    return new Promise<User>((resolve) => {
      setTimeout(() => {
        resolve({
          id:1,
          username: username,
          real_name: '演示用户',
          email: 'demo@example.com',
          phone: '13800138000',
          is_superuser: true,
          status: true,
          department_id: 1,
          created_at: new Date().toISOString()
        } as User)
      }, 300)
    })
  },
  
  /**
   * 更新当前用户信息
   * @param data 部分用户信息
   * @returns 更新后的用户信息
   */
  updateCurrentUser(data: Partial<User>) {
    return request.put<User>('/auth/me', data)
  }
}
