import axios from "axios";

axios.defaults.timeout = 2000;
const backendUrl = process.env?.REACT_APP_BACKEND_URL || "localhost";

const API_URL = `http://${backendUrl}:5000`;


export const isAPIup = async () => {
  try {
    await axios.get(`${API_URL}/up`, {
      timeout: 2000
    });
    return true;
  } catch (error) {
    console.log(`Error occurred when '${API_URL}/up'`);
    if (error.code === 'ECONNABORTED') {
      console.log(`Request timed out for '${API_URL}/up'`);
    } else {
      console.log(error.message);
    }
    return false;
  }
};


export const tryLogin = async (email,password) => {
  const loginData = {
    email: email,
    password: password
  };

  try {
    const response = await axios.post(`${API_URL}/login`, loginData);
    return ["Login successfull", response.data];

  } catch (error) {
    if(error?.response?.status === 401)
      return ["Incorrect credentials", null];
    else
      return ["API unavailable", null];
  }
};

export const getAllUsers = async (token) => {

  try {
    const response = await axios.get(`${API_URL}/users`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    return response.data;
  } catch (error) {
    if(error?.response?.status === 403)
      throw new Error("Access forbidden");
    else
      throw new Error("API unavailable");
  }

};
