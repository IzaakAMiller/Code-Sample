const blastPath = "http://localhost:8001/blast";

import ApiClient from "../../../api/apiclient";

export default class BlastService {

    static async runBlastQuery(blastJobData) {
        return await ApiClient.doPost(blastPath, blastJobData);
    }

    static async retrieveBlastResults() {
        return await ApiClient.doGet(blastPath);
    }
}
