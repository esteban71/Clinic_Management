import './App.css';
import {Route, Routes} from 'react-router-dom';
import Layout from './components/Layout';
import Public from './components/Public';
import Login from './features/auth/Login'
import DashLayout from './components/DashLayout';
import Welcome from './features/auth/Welcome';
import PatientsList from './features/patients/PatientsList'
import EditPatient from './features/patients/EditPatient'
import NewPatient from './features/patients/NewPatient'
import MedecinsList from './features/medecin/MedecinsList.jsx';
import Prefetch from './features/auth/Prefetch.jsx'
import PersistLogin from './features/auth/PersistLogin.jsx';
import RequireAuth from './features/auth/RequireAuth.jsx';
import {Roles} from './config/roles.jsx'
import EditMedecins from "./features/medecin/EditMedecins.jsx";
import NewDoctor from "./features/medecin/NewDoctor.jsx";
import ReceptionistList from "./features/Receptionist/ReceptionistList.jsx";
import EditReceptionist from "./features/Receptionist/EditReceptionist.jsx";
import NewReceptionist from "./features/Receptionist/NewReceptionist.jsx";


function App() {
  return (
    <Routes>
      <Route path='/' element={<Layout />} >
        {/* Public Routes */}
        <Route index element={<Public />} />
        <Route path='login' element={<Login />} />
        
        {/* Protected routes */}
        <Route element={<PersistLogin/>}>
          <Route element={<RequireAuth allowedRoles={[...Object.values(Roles)]} />}>
            <Route element={<Prefetch />}>
              <Route path='dash' element={<DashLayout/>}>

                <Route index element={<Welcome />} />

                <Route path='patients'>
                  <Route index element={<PatientsList />} />
                  <Route path=':id' element={<EditPatient />} />
                  <Route element={<RequireAuth allowedRoles={[Roles.Manager, Roles.admin, Roles.Receptionist]} />}>
                    <Route path='new' element={<NewPatient />} />
                  </Route>
                </Route>

                <Route element={<RequireAuth allowedRoles={[Roles.Manager, Roles.admin, Roles.Receptionist]} />}>
                    <Route path='receptionists'>
                        <Route index element={<ReceptionistList/>}/>
                        <Route path=':id' element={<EditReceptionist/>}/>
                        <Route path='new' element={<NewReceptionist/>}/>
                  </Route>
                </Route>

                <Route element={<RequireAuth allowedRoles={[Roles.Manager, Roles.admin, Roles.Receptionist]} />}>
                  <Route path='medecins'>
                    <Route index element={<MedecinsList/>}/>
                    <Route path=':id' element={<EditMedecins/>}/>
                    <Route path='new' element={<NewDoctor/>}/>
                  </Route>
                </Route>

              </Route> {/* End Dash */}
            </Route>
          </Route> {/* End of protected routes */}
        </Route> 

      </Route>
    </Routes>
  );
}

export default App;
