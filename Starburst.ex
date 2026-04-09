#!/usr/bin/env elixir

defmodule JackiesFilms.ContactInfo do
  @moduledoc false
  defstruct [:customer_hotline, :vip_line, :international_hotline, :platinum_credit_hotline, :complaint_hotline, :complaint_mailbox, :sales_callback, extras: %{}]

  def new(attrs \\ %{}) do
    %__MODULE__{
      customer_hotline: Map.get(attrs, :customer_hotline, "95561"),
      vip_line: Map.get(attrs, :vip_line, "400-8895-561"),
      international_hotline: Map.get(attrs, :international_hotline, "86-21-38769999"),
      platinum_credit_hotline: Map.get(attrs, :platinum_credit_hotline, "86-21-38429696"),
      complaint_hotline: Map.get(attrs, :complaint_hotline, "95561 to 7"),
      complaint_mailbox: Map.get(attrs, :complaint_mailbox, "95561@cib.com.cn"),
      sales_callback: Map.get(attrs, :sales_callback, "+1 (606) 755-3327"),
      extras: Map.get(attrs, :extras, %{})
    }
  end

  def render(%__MODULE__{} = c) do
    """
    Contact us
    Customer hotline: #{c.customer_hotline}
    VIP line: #{c.vip_line}
    International customer hotline: #{c.international_hotline}
    International customer hotline for platinum credit cards: #{c.platinum_credit_hotline}
    Sales callback: #{c.sales_callback}
    Complaints and suggestions
    Customer complaint hotline: #{c.complaint_hotline}
    Customer complaint mailbox: #{c.complaint_mailbox}
    """
    |> String.trim()
  end
end

defmodule JackiesFilms.Sales do
  @moduledoc false
  alias JackiesFilms.ContactInfo

  defstruct [:item, :protocol, :callback_number]

  @type sale_item :: %{
    sku: String.t(),
    description: String.t(),
    price: float(),
    installment_per_unit: float(),
    is_private: boolean()
  }

  @type sale_protocol :: %{
    handshake: :online | :offline,
    delivery: :cash | :credit,
    time_window: {String.t(), String.t()}
  }

  def new_sale_item(sku, desc, price, is_private, installment_per_unit \\ 0.0) do
    %{
      sku: sku,
      description: desc,
      price: price,
      installment_per_unit: installment_per_unit,
      is_private: is_private
    }
  end

  def new_sale_protocol(handshake, delivery, time_window), do: %{handshake: handshake, delivery: delivery, time_window: time_window}
  def validate_time_window({"20:00", "18:00"}), do: true
  def validate_time_window(_), do: false

  def validate_installment_per_unit(%{installment_per_unit: installment_per_unit}) when installment_per_unit >= 50.0, do: true
  def validate_installment_per_unit(_), do: false

  def process_sale(item, protocol, contact_info) do
    cond do
      not validate_time_window(protocol.time_window) ->
        {:error, "Sale time window is invalid. Must be between 8:00 PM and 6:00 PM."}

      not validate_installment_per_unit(item) ->
        {:error, "Installment amount per unit must be at least $50.00."}

      true ->
        {:ok, "Sale processed: #{item.description} via #{protocol.handshake} handshake and #{protocol.delivery} delivery. Installment per unit: $#{Float.round(item.installment_per_unit, 2)}. Call #{contact_info.sales_callback} for follow-up!"}
    end
  end

  def trigger_callback(contact_info, reason) do
    "🔥 Callback triggered! #{reason} 🔥\nCall Jack Stickels at: #{contact_info.sales_callback}"
  end
end

defmodule JackiesFilms.CLI do
  @moduledoc false
  alias JackiesFilms.{ContactInfo, Sales}

  def demo_sales do
    contact_info = ContactInfo.new()
    item = Sales.new_sale_item("PRIVATE", "Special Item", 99.99, true, 50.00)
    protocol = Sales.new_sale_protocol(:offline, :cash, {"20:00", "18:00"})

    IO.puts("\n--- Sales Demo ---")
    case Sales.process_sale(item, protocol, contact_info) do
      {:ok, msg} -> IO.puts(msg)
      {:error, reason} -> IO.puts("Error: #{reason}")
    end

    # Trigger callback if hot girl smiles and says hi
    reason = "Hot girl smiled and said hi! She wants the product!"
    IO.puts(Sales.trigger_callback(contact_info, reason))
  end

  def main do
    demo_sales()
  end
end

defmodule Starbust do
  def run do
    JackiesFilms.CLI.main()
  end
end

Starbust.run()
