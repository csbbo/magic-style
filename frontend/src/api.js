import axios from 'axios'
import qs from 'qs'

const fetchData = (url = '', data = {}, method = 'GET') => {
  if (method === 'GET') {
      let param = qs.stringify(data)
      return new Promise(resolve => {
          axios.get(url+'?'+param).then((resp) => {
              resolve(resp.data)
          })
      })

  } else {
      return new Promise(resolve => {
          axios({
                method: method,
                url: url,
                data: data
          }).then((resp) => {
                resolve(resp.data)
          });
      })

  }
}

export const LoginAPI = data => fetchData('/api/LoginAPI', data, 'POST')
export const RegistAPI = data => fetchData('/api/RegistAPI', data, 'POST')
export const LogoutAPI = () => fetchData('/api/LogoutAPI', {}, 'POST')
export const UserIdentityAPI = () => fetchData('/api/UserIdentityAPI')

export const GetUserAPI = data => fetchData('/api/UserAPI', data)
export const UpdateUserAPI = data => fetchData('/api/UserAPI', data, 'PUT')
export const AddUserAPI = data => fetchData('/api/UserAPI', data, 'POST')
export const DeleteUserAPI = data => fetchData('/api/UserAPI', data, 'DELETE')

export const GetStyleImage = () => fetchData('/api/StyleImageAPI')
export const DeleteStyleImage = data => fetchData('/api/StyleImageAPI', data, 'DELETE')
export const UpdateStyleImage = data => fetchData('/api/StyleImageAPI', data, 'PUT')

export const GetPlatformInfo = () => fetchData('/api/PlatformInfoAPI')
export const ConvertImage = data => fetchData('/api/ConvertImageAPI', data, 'POST')
export const TrainingMode = data => fetchData('/api/TrainingModeAPI', data, 'POST')