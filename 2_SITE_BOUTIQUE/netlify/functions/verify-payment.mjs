import crypto from "node:crypto";
import Stripe from "stripe";

const PRICES = Object.freeze({
  semaine: "price_1UVq9u4B9y6vJovVJbXzpLuT",
  mois: "price_1UVqD44B9y6vJovVO0gjgpE6",
  trimestre: "price_1UWCow4B9y6vJovV9QaSHDy5",
  lifetime: "price_1UVr7K4B9y6vJovVCaXgbHJo"
});

const json = (data, status = 200) => Response.json(data, {
  status,
  headers: { "Cache-Control": "no-store" }
});

const makeLicense = () => {
  const raw = crypto.randomBytes(9).toString("hex").toUpperCase();
  return `ARCEUS-${raw.slice(0, 6)}-${raw.slice(6, 12)}-${raw.slice(12, 18)}`;
};

export default async (request) => {
  if (request.method !== "POST") return json({ error: "Méthode refusée." }, 405);
  if (!process.env.STRIPE_SECRET_KEY) return json({ error: "Stripe n'est pas configuré sur le serveur." }, 500);

  try {
    const { paymentIntentId } = await request.json();
    if (!/^pi_[A-Za-z0-9_]+$/.test(paymentIntentId || "")) return json({ error: "Paiement invalide." }, 400);

    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
    let intent = await stripe.paymentIntents.retrieve(paymentIntentId);
    const plan = intent.metadata.plan;

    if (intent.status !== "succeeded") return json({ error: "Le paiement n'est pas confirmé." }, 402);
    if (!plan || PRICES[plan] !== intent.metadata.price_id) return json({ error: "Le tarif payé ne correspond pas à l'offre." }, 409);

    let licenseKey = intent.metadata.license_key;
    if (!licenseKey) {
      licenseKey = makeLicense();
      intent = await stripe.paymentIntents.update(intent.id, {
        metadata: { ...intent.metadata, license_key: licenseKey }
      });
      licenseKey = intent.metadata.license_key;
    }

    return json({ key: licenseKey, plan });
  } catch (error) {
    console.error("verify-payment", error);
    return json({ error: "Impossible de vérifier le paiement Stripe." }, 500);
  }
};
