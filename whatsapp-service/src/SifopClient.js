const https = require("https");
const axios = require("axios");

const { SIFOP_URL, SIFOP_TOKEN } = require("./config");

class SifopClient {

    constructor() {

        this.client = axios.create({

            baseURL: SIFOP_URL,

            httpsAgent: new https.Agent({
                rejectUnauthorized: false
            }),

            headers: {
                Authorization: `Bearer ${SIFOP_TOKEN}`
            }

        });
    }

    async health() {

        const response =
            await this.client.get("/health");

        return response.data;
    }

    async buscarTerceirizadoPorId(id) {

        const response =
            await this.client.get(`/terceirizados/${id}`);

        return response.data;
    }

    async buscarUsuarioPorMatricula(matricula) {

        const response =
            await this.client.get(`/usuarios/matricula/${matricula}`);

        return response.data;
    }

    async gerarFolha(tipo, id, mes) {

        const response =
            await this.client.post(
                "/folha/pdf",
                {
                    tipo,
                    id,
                    mes
                },
                {
                    responseType: "arraybuffer"
                }
            );

        return Buffer.from(response.data);
    }
}

module.exports = new SifopClient();