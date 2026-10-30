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

export default async (request) => {
  if (request.method !== "POST") return json({ error: "Méthode refusée." }, 405);
  if (!process.env.STRIPE_SECRET_KEY) return json({ error: "Stripe n'est pas configuré sur le serveur (clé secrète manquante)." }, 500);

  try {
    const { plan } = await request.json();
    const priceId = PRICES[plan];
    if (!priceId) return json({ error: `Offre inconnue (${plan}).` }, 400);

    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
    const price = await stripe.prices.retrieve(priceId, { expand: ["product"] });

    console.log(`[Stripe] Récupération tarif ${priceId} pour l'offre ${plan}:`, {
      active: price.active,
      type: price.type,
      currency: price.currency,
      unit_amount: price.unit_amount
    });

    if (!price) {
      return json({ error: `Le tarif Stripe (${priceId}) est introuvable.` }, 404);
    }

    if (!price.active) {
      return json({ error: `Le tarif Stripe (${priceId}) est marqué inactif/archivé dans votre tableau de bord Stripe.` }, 409);
    }

    const amount = price.unit_amount || (price.unit_amount_decimal ? Math.round(Number(price.unit_amount_decimal)) : null);
    if (!amount || amount <= 0) {
      return json({ error: `Le tarif Stripe (${priceId}) n'a pas de montant valide configuré.` }, 409);
    }

    const currency = (price.currency || "eur").toLowerCase();

    const intent = await stripe.paymentIntents.create({
      amount: amount,
      currency: currency,
      automatic_payment_methods: { enabled: true },
      metadata: {
        plan,
        price_id: price.id,
        product_id: typeof price.product === "string" ? price.product : (price.product?.id || "")
      },
      description: `ARCEUS - ${plan}`
    });

    return json({
      clientSecret: intent.client_secret,
      paymentIntentId: intent.id,
      amount: amount,
      currency: currency
    });
  } catch (error) {
    console.error("create-payment-intent error:", error);
    return json({ error: error.message || "Impossible de préparer le paiement Stripe." }, 500);
  }
};
