import React from 'react'
import { useParams } from 'react-router-dom'
import { useSelector } from 'react-redux'
import { selectUserById } from './usersApiSlice.jsx'
import EditUserForm from './EditUserForm'
import CircularLoader from '../../pageLoader/CircularLoader.jsx'

const EditUser = () => {

  const { id } = useParams()

  const user = useSelector(state => selectUserById(state, id))

  const content = user ? <EditUserForm user={user} /> : <CircularLoader />

  return content
  
}

export default EditUser
