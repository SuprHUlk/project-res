import axios from "axios";
import { Response } from "../model/response";

const BASE_URL = "http://localhost:8000";

const upsertHeaders = (headersToAdd: {} = {}) => {
    let headers = {
        "Content-Type": "application/json",
        ...headersToAdd,
    };

    return headers;
};

export const post = async (
    endpoint: string,
    payload: {},
    customHeaders: {} = {}
): Promise<Response<any>> => {
    try {
        const res = await axios.post(BASE_URL + endpoint, payload, {
            headers: upsertHeaders(customHeaders),
            withCredentials: true,
        });
        return res.data;
    } catch (e) {
        console.error("POST request failed:", e);
        throw e;
    }
};

export const get = async (
    endpoint: string,
    customHeaders: {} = {}
): Promise<Response<any>> => {
    try {
        const res = await axios.get(BASE_URL + endpoint, {
            headers: upsertHeaders(customHeaders),
            withCredentials: true,
        });

        return res.data;
    } catch (e) {
        console.log("GET request failed:", e);
        throw e;
    }
};
