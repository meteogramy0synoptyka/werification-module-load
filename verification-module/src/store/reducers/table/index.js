import { ADD_DATA, UPDATE_SLOPE, UPDATE_INTERCEPT } from "./actions";

const defaultState = {
  slope: 0.15,
  intercept: 0.15,
  data: {},
};

export function table(state = defaultState, action) {
  switch (action.type) {
    case ADD_DATA:
      return {
        ...state,
        data: {
          ...state.data,
          ...action.payload,
        },
      };
    case UPDATE_SLOPE:
      return {
        ...state,
        slope: action.slope,
      };
    case UPDATE_INTERCEPT:
      return {
        ...state,
        intercept: action.intercept,
      };
    default:
      return state;
  }
}
