import React, {useState,useEffect} from "react";
import { Card } from "../Card/card";

const TodoPage = () => {

//todo is a state variable, setTodo a setter for this state variable 
// this way you could try to get the exercise metadata 
  const [todo, setTodo] = useState([]) 

  useEffect(() => {
      fetch('/api').then(response => {
          if(response.ok) {
              return response.json()
          }
  }).then(data => console.log(data[0].content))
},[])

  return (
    <>
      <Card listOfTodos={todo}/>
    </>
  )
}

export default TodoPage
