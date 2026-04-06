# Test campaign: image generation + HypeEngine (two slots)

**Purpose:** End-to-end check — branded **`post-image.png`** (via **`auto-image-generation`**) → **`post-bundle.md`** → **`hype-engine`** publish. **Two posts** = two **different** calendar rows (09:00 and 18:00), not the same row twice.

**Idempotency:** After a row shows **`HypeEngine post UUID`** in **`APPROVAL.md`**, do not create another HypeEngine post for that **Post ID** unless a human clears the UUID.

## Steps (OpenClaw GUI)

1. Run **`auto-image-generation`** for **`posts/test-001/`** then **`posts/test-002/`** (read `post-body.md`, **`brand-images/`** / `BRAND_IMAGES_DIR`, write **`post-image.png`** + **`image-alt.txt`**).
2. Run **`social-media-manager`**: fill **`post-bundle.md`** for each post; ensure **`APPROVAL.md`** has empty **HypeEngine post UUID** until first successful publish.
3. Approve rows → run **`hype-engine`** once per row; **record UUIDs** in **`APPROVAL.md`**.
4. Re-run publish agent → should **skip** both rows (UUIDs set).

**Optional:** Set **`BRAND_IMAGES_DIR`** if brand kit is not under `workspace/brand-images/`.
