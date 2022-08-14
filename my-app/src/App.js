import Header from './components/Header'
import ExBox from './components/ExBox';
import InstructionBox from './components/InstructionBox';
import AnswerZone from './components/AnswerZone';
import TodoPage from './components/Page/TodoPage';
import { useEffect,useState } from 'react';
import RSSelector from './components/RSSelector';
import Switch from './components/Switch';
import TutorialHeader from './components/TutorialHeader';


function App() {
  const [exerciseID, setExerciseID] = useState(16)
  const [exercise, setExercise] = useState([])
  const [studentAnswers, setStudentAnswers] = useState()
  const [loadingPage, setLoadingPage] = useState(false)
  const [traRSToggled, settraRSToggled] = useState(true)
  const [tutorialPage, setTutorialPage] = useState(true)
  const [listOfTutorialIDs, setListOfTutorialIDs] = useState([63, 64, 65, 66, 67, 68, 69, 70, 71, 72])
  const [tutorialID, setTutorialID] = useState(63)

  // const [instruction, setInstruction] = useState()


  // hier id nog bij toevoegen
  useEffect(() => {
    fetch('/exercises').then(response => {
        if(response.ok) {
            return response.json()
        }
}).then(data => setExercise(data[exerciseID-1]))
},[exerciseID])

  useEffect(() => {
    fetch('/exercises').then(response => {
        if(response.ok) {
            return response.json()
        }
  }).then(data => setExercise(data[tutorialID-1]))
  },[tutorialID])


  const transferStudentAnswers =  (studAnswers) =>  {
    console.log('student answers updated to' , studAnswers)
    setStudentAnswers(studAnswers)
    console.log('these are the student answers' , studentAnswers)
  } 


  // const transferRSSelection = () => {
  //   console.log('before changing state of RS = ', adaptiveFadingRS )
  //   setAdaptiveFadingRS(!adaptiveFadingRS)
  //   console.log('after changing state of RS', adaptiveFadingRS)
  // }


  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('you presseed the button')
    console.log(studentAnswers)
    setLoadingPage(true)
    fetch('/studentInfo', { 
      method: 'PUT',
      body: JSON.stringify({
        content: studentAnswers,
        recommender: traRSToggled
      }),
      headers: {
        "Content-Type": "application/json; charset = UTF-8"
      }
    }).then(response => response.json())
    .then(message => setExerciseID(message['answer']))
    console.log('we are at the end of the submit')
    console.log(exerciseID)
    setLoadingPage(false)
    
    // this would be the place to get the next exercise from the back - end

  }

  const handleToggle = (e) => {
    e.preventDefault();
    console.log('loadingpage has been set')
    setLoadingPage(true)

    settraRSToggled(! traRSToggled)
    
    fetch('/studentInfo', { 
      method: 'PUT',
      body: JSON.stringify({
        content: 'initialization',
        recommender: traRSToggled
      }),
      headers: {
        "Content-Type": "application/json; charset = UTF-8"
      }
    }).then(response => response.json())
    .then(message => console.log(message['answer']))
    const next_ex = getStartId(traRSToggled)
    setExerciseID(next_ex)
    setLoadingPage(false)
  }

  function getStartId(traRSToggled){
    console.log('start calculation of next exercise')
    var sol = 4
    if (traRSToggled == false) {
      sol = 16
    }
    console.log('the first exercise after initialization will be', sol)
    return sol
  }

  function arrayRemove(arr, value) { 
    
    return arr.filter(function(ele){ 
        return ele != value; 
    });
  }

  function recommendNextTutorialExercise() {
    var cur_ID = tutorialID
    var new_list = arrayRemove(listOfTutorialIDs,cur_ID)
    var nextID = new_list[0]
    setListOfTutorialIDs(new_list)
    setTutorialID(nextID)
  }

  return (
    <>
    {tutorialPage === true && loadingPage === false &&
    <>
      <div>
        <TutorialHeader/>
      </div>
      <div className="container">
        <Header/>
        {/* <RSSelector transferRSSelection = {transferRSSelection}/> */}
        <Switch traRSToggled ={traRSToggled} onToggle = {handleToggle} />
        <InstructionBox exerciseToShow = {exercise}/>
        <ExBox exerciseToShow = {exercise} transferStudentAnswers={transferStudentAnswers}/>
        <div className='answerZone'> 
          <button className= 'button-tutor' onClick={recommendNextTutorialExercise}>
            Submit Answer
          </button>
        </div>
      </div>
      <div className=' directToModuleZone'>
          <button className = "goToModule-btn" onClick={() => setTutorialPage(false)}>
            Let's start the study!
          </button>
      </div>
    </>
    }

    {loadingPage === false && tutorialPage === false &&
      <div className="container">
        <Header/>
        {/* <RSSelector transferRSSelection = {transferRSSelection}/> */}
        <Switch traRSToggled ={traRSToggled} onToggle = {handleToggle} />
        <InstructionBox exerciseToShow = {exercise}/>
        <ExBox exerciseToShow = {exercise} transferStudentAnswers={transferStudentAnswers}/>
        <div className='answerZone'> 
          <button className="button" onClick={handleSubmit}>
            Submit Answer
          </button>
        </div>
        
      </div>
    }

    {loadingPage === true && tutorialPage === false &&
    <div className='container'>
      <h1>
        Next exercise is being calculated.
      </h1>
    </div>
    }

    </>
  );
    
}

// function App() {
//   return (
//     <div>
//       <TodoPage/>
//     </div>
//   );
// }

  // const handleSubmit = (e) => {
  //   e.preventDefault();
  //   console.log('you presseed the button')
  //   fetch('/studentInfo').then(response =>{
  //     if (response.ok) {
  //       console.log(response.json()['mastery_SPrP'])
  //       return response.json()
  //     }
  //   })
  // }

//   useEffect(() => {
//     fetch('/exercises').then(response => {
//         if(response.ok) {
//             return response.json()
//         }
// }).then(data => setExercise(data[0]))
// },[])

export default App;
