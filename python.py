import time
from dotenv import load_dotenv
from console import ConsoleController
from model import ModelHandler

load_dotenv()

models = [
        'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3',
        'meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d'
    ]


prompt = """
[INST]
The subject of this prompt is within the [CODE][/CODE]  tags.
Check the comments within the <RETURNABLE> tags in the given piece of [CODE]. 
Only return the text within <RETURNABLE></RETURNABLE> blocks. 
Comments are not code. Do not add or change any code. COMMENTS ONLY.  
Do not add any new comments. UPDATE EXISTING COMMENTS ONLY. 
EXAMPLE:
If I send you the following Typescript code: 
<RETURNABLE> 
/**
 * Adds two numbers and returns the result.
 * @param num1 - The first number to be added.
 * @param num2 - The second number to be added.
 * @returns The sum of the two numbers.
 */
function addNumbers(num1: number, num2: number): number {
</RETURNABLE> 
  return num1 + num2;
}
You MUST return it in the following format:
<NEWCOMMENT>
/**
  * Adds two numbers and returns the result.
  * @param num1 - The first number to be added.
  * @param num2 - The second number to be added.
  * @returns The sum of the two numbers.
*/
function addNumbers(num1: number, num2: number): number {
</NEWCOMMENT> 
If you find multiple <RETURNABLE> blocks, you must return them in the same order as they appear in the code.
This would look like this:
<NEWCOMMENT>
{The updated RETURNABLE block}
</NEWCOMMENT>
<NEWCOMMENT>
{The updated RETURNABLE block}
</NEWCOMMENT>


Now go ahead and process the following code within the [CODE] tags:
[/INST]
[CODE]
${code}
[/CODE]
"""

code = """
import { Controller, Get, Param, Post, Query } from '@nestjs/common';
import { DateTime } from 'luxon';
import { Authenticated } from '~/auth/authenticated.decorator';
import { Hour, HourService } from '~/domain';
import { CreateInvoiceDto, CreateInvoiceLineDto, InvoiceDto, SimplicateAdapter } from '~/infrastructure/simplicate';

interface CrossInvoiceServiceHours {
  name: string;
  totalAmount: number;
  totalDuration: number;
  hours: Hour[];
}

interface CrossInvoiceProjectHours {
  name: string;
  totalAmount: number;
  totalDuration: number;
  services: CrossInvoiceServiceHours[];
}

interface CrossInvoiceHours {
  vendorId: string;
  vendorName: string;
  supplierId: string;
  supplierName: string;
  supplierMyOrganizationProfileId: string;
  totalAmount: number;
  totalDuration: number;
  projects: CrossInvoiceProjectHours[];
}

<RETURNABLE>
/**
 * This is the MoneyController class which handles API requests related to hours.
 */
@Authenticated()
@Controller('api/hours')
export class HourController {
</RETURNABLE>
  constructor(private readonly service: HourService, private readonly simplicate: SimplicateAdapter) {}

  @Get('date/:start/:end')
  getRange(@Param('start') start: string, @Param('end') end: string) {
    const startDate = DateTime.fromFormat(start, 'yyyy-MM-dd');
    const endDate = DateTime.fromFormat(end, 'yyyy-MM-dd').endOf('day');

    return this.service.find(startDate, endDate);
  }
  
  <RETURNABLE>
  /**
   * Retrieves the months data based on the provided week year and week number.
   *
   * @param weekYear - The year of the week.
   * @param weekNumber - The number of the week.
   * @returns The data for the specified week.
   */
  @Get('week/:weekYear/:weekNumber')
  getWeek(@Param('weekYear') weekYear: number, @Param('weekNumber') weekNumber: number) {
  </RETURNABLE>
    const startDate = DateTime.fromObject({ weekYear, weekNumber }).startOf('week');
    const endDate = startDate.endOf('week');
    return this.service.find(startDate, endDate);
  }

  @Get('month/:year/:month')
  async getMonth(@Param('year') year: number, @Param('month') month: number) {
    const startDate = DateTime.fromObject({ year, month, day: 1 });
    const endDate = startDate.endOf('month');

    return this.service.find(startDate, endDate);
  }

  @Post('cross/invoices/:year/:month')
  async createInvoices(@Param('year') year: number, @Param('month') month: number): Promise<void> {
    const invoiceData = await this.collectInvoiceData(year, month);
    await Promise.all(invoiceData.invoices.map((data) => this.simplicate.postInvoice(data)));
  }

  @Get('cross/invoices/:year/:month')
  async collectInvoiceData(
    @Param('year') year: number,
    @Param('month') month: number
  ): Promise<{ invoiced: CrossInvoiceHours[]; uninvoiced: CrossInvoiceHours[]; invoices: InvoiceDto[] }> {
    const invoiced = await this.getCross(year, month, { invoiced: true });
    const uninvoiced = await this.getCross(year, month, { uninvoiced: true });
    const invoices = await Promise.all(
      invoiced.map(async (cross) => {
        const my_organization_profile_id = cross.supplierMyOrganizationProfileId;
        const organization = await this.simplicate.getOrganization(cross.vendorId);
        const payment_term_id = organization.debtor?.payment_term.id;
        const vat_class = await this.simplicate.getVatClass('0%');
        const status = await this.simplicate.getInvoiceStatus('Draft');
        const revenue_group = await this.simplicate.getRevenueGroup('Algemeen');
        const invoice_lines: CreateInvoiceLineDto[] = cross.projects.flatMap((project) =>
          project.services.map((service) => ({
            date: DateTime.now().toFormat('yyyy-MM-dd'),
            description: project.name + ': ' + service.name,
            amount: service.totalDuration,
            price: service.totalAmount / service.totalDuration,
            vat_class_id: vat_class.id,
            revenue_group_id: revenue_group.id,
          }))
        );
        <RETURNABLE>
        const organization_id = cross.vendorId; // replace man.vendorId with cross.vendorId at a later point 
        </RETURNABLE>
        const status_id = status.id;
        const invoice: CreateInvoiceDto = {
          date: DateTime.now().toFormat('yyyy-MM-dd'),
          subject: `Werkzaamheden van ${cross.supplierName} voor ${cross.vendorName} in ${year}-${month}`,
          reference: `INF-CROSS-${year}-${month}`,
          my_organization_profile_id,
          organization_id,
          payment_term_id,
          invoice_lines,
          status_id,
          sending_method: 'email',
        };
        return invoice;
      })
    );
    return { invoiced, uninvoiced, invoices };
  }

  @Get('cross/:year/:month')
  async getCross(
    @Param('year') year: number,
    @Param('month') month: number,
    @Query() query: { invoiced?: unknown; uninvoiced?: unknown }
  ): Promise<CrossInvoiceHours[]> {
    const startDate = DateTime.fromObject({ year, month, day: 1 });
    const endDate = startDate.endOf('month');
    const showInvoicedOnly = 'invoiced' in query;
    const showUninvoicedOnly = 'uninvoiced' in query;
    const hours = await this.service.find(startDate, endDate);
    return hours
      .filter(
        (hour) =>
          hour.vendorId &&
          hour.vendorId !== hour.supplierId &&
          (!(showInvoicedOnly || showUninvoicedOnly) ||
            (showInvoicedOnly && hour.isInvoiced) ||
            (showUninvoicedOnly && !hour.isInvoiced))
      )
      .reduce<CrossInvoiceHours[]>((accu, hour) => {
        let invoice = accu.find((i) => i.vendorName === hour.vendorName && i.supplierName === hour.supplierName);
        if (!invoice) {
          invoice = {
            vendorId: hour.vendorId,
            vendorName: hour.vendorName,
            supplierName: hour.supplierName,
            supplierId: hour.supplierId,
            supplierMyOrganizationProfileId: hour.supplierMyOrganizationProfileId,
            totalAmount: 0,
            totalDuration: 0,
            projects: [],
          };
          accu.push(invoice);
        }
        let project = invoice.projects.find((p) => p.name === hour.customerName + ':' + hour.projectName);
        if (!project) {
          project = {
            name: hour.customerName + ':' + hour.projectName,
            totalDuration: 0,
            totalAmount: 0,
            services: [],
          };
          invoice.projects.push(project);
        }
        let service = project.services.find((s) => s.name == hour.serviceName + ' @ ' + hour.rate);
        if (!service) {
          service = { name: hour.serviceName + ' @ ' + hour.rate, totalDuration: 0, totalAmount: 0, hours: [] };
          project.services.push(service);
        }

        const { durationHours, rate } = hour;
        invoice.totalAmount += durationHours * rate;
        invoice.totalDuration += durationHours;
        project.totalAmount += durationHours * rate;
        project.totalDuration += durationHours;
        service.totalAmount += durationHours * rate;
        service.totalDuration += durationHours;
        service.hours.push(hour);

        return accu;
      }, []);
  }
}

"""
prompt = prompt.replace('${code}', code)



def check_predictions_status(handlers):
    for handler in handlers:
        handler.prediction.reload()
        handler.update_time_variables()

    return all(handler.prediction.status == "succeeded" for handler in handlers)


def main():
    console_controller = ConsoleController()
    handlers = [ModelHandler(model_id, prompt, console_controller) for model_id in models]

    console_controller.print_and_save_total_start_time()
    for handler in handlers:
        handler.create_prediction()

    # Wait for predictions to complete
    while not check_predictions_status(handlers):
        time.sleep(0.2)
        [handler.print_prediction_status() for handler in handlers]

    print('\n')
    console_controller.print_end_result(handlers)


if __name__ == '__main__':
    main()
