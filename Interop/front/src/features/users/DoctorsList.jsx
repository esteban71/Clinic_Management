import React from 'react'
import { useGetusersQuery } from './usersApiSlice.jsx'
import User from './User'
import useAuth from '../../hooks/useAuth.jsx'
import CircularLoader from '../../pageLoader/CircularLoader.jsx'
import '../../css/userList.css'

const DoctorsList = () => {

  const { isManager, isAdmin, isReceptionist } = useAuth()

  const {
    data: users,
    isLoading,
    isSuccess,
    isError,
    error
  } = useGetusersQuery('usersList', {
    pollingInterval: 60000,
    refetchOnFocus: true,
    refetchOnMountOrArgChange: true
  })

  console.log(users)

  let content

  if(isLoading) {
    content = (
      <CircularLoader />
    )
  }

  if(isError) {
    content = <p className='errmsg'> {error?.data?.message} </p>
  }

  if(isSuccess) {
    const { ids, entities } = users

    let entitiesArray = Object.values(entities)

    let tableContent
    
    if(isManager || isAdmin || isReceptionist) {
      tableContent = entitiesArray?.length 
      ? entitiesArray.filter(user => user.roles[0] === 'Doctor')
      .map(user => <User key={user.id} userId={user.id} />)
      : null
    }


    content = (
      <table className='table_userlist'>
        <thead className='table__thead'>
          <tr>
            <th scope='col' className="table__th table__Uppercase">name</th>
            <th scope='col' className="table__th table__Uppercase">username</th>
            <th scope='col' className="table__th table__Uppercase">Role</th>
            <th scope='col' className="table__th table__Uppercase">View/Edit</th>
          </tr>
        </thead>

        <tbody>
            { tableContent }
        </tbody>
      </table>
    )
  }

  return content

}

export default DoctorsList

